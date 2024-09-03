# Copyright 2024 Niels Provos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import threading
import time
from collections import defaultdict, deque
from queue import Empty, Queue
from threading import Event, Lock
from typing import (
    TYPE_CHECKING,
    DefaultDict,
    Deque,
    Dict,
    Generator,
    List,
    Optional,
    Tuple,
)

from .task import Task, TaskWorker
from .web_interface import is_quit_requested, run_web_interface

if TYPE_CHECKING:
    from .graph import Graph


# Type aliases
TaskID = int
TaskName = str
ProvenanceChain = Tuple[Tuple[TaskName, TaskID], ...]


class Dispatcher:
    def __init__(self, graph: "Graph", web_port=5000):
        self.graph = graph
        self.work_queue = Queue()
        self.provenance: DefaultDict[ProvenanceChain, int] = defaultdict(int)
        self.notifiers: DefaultDict[ProvenanceChain, List[TaskWorker]] = defaultdict(
            list
        )
        self.provenance_lock = Lock()
        self.notifiers_lock = Lock()
        self.stop_event = Event()
        self.active_tasks = 0
        self.task_completion_event = threading.Event()
        self.web_port = web_port
        self.debug_active_tasks: Dict[int, Tuple[TaskWorker, Task]] = {}
        self.completed_tasks: Deque[Tuple[TaskWorker, Task, str]] = deque(
            maxlen=100
        )  # Keep last 100 completed tasks
        self.failed_tasks: Deque[Tuple[TaskWorker, Task]] = deque(
            maxlen=100
        )  # Keep last 100 failed tasks
        self.total_completed_tasks = 0
        self.total_failed_tasks = 0
        self.task_id_counter = 0
        self.task_lock = threading.Lock()

    def _generate_prefixes(self, task: Task) -> Generator[Tuple, None, None]:
        provenance = task._provenance
        for i in range(1, len(provenance) + 1):
            yield tuple(provenance[:i])

    def _add_provenance(self, task: Task):
        for prefix in self._generate_prefixes(task):
            with self.provenance_lock:
                self.provenance[prefix] = self.provenance.get(prefix, 0) + 1

    def _remove_provenance(self, task: Task):
        to_notify = set()
        for prefix in self._generate_prefixes(task):
            with self.provenance_lock:
                self.provenance[prefix] -= 1
                if self.provenance[prefix] == 0:
                    del self.provenance[prefix]
                    to_notify.add(prefix)

        for prefix in to_notify:
            self._notify_task_completion(prefix, task)

    def watch(
        self, prefix: ProvenanceChain, notifier: TaskWorker, task: Optional[Task] = None
    ) -> bool:
        """
        Watches the given prefix and notifies the specified notifier when the prefix is no longer tracked
        as part of the provenance of all tasks.

        This method sets up a watch on a specific prefix in the provenance chain. When the prefix is
        no longer part of any task's provenance, the provided notifier will be called with the prefix
        as an argument. If the prefix is already not part of any task's provenance, the notifier may
        be called immediately.

        Parameters:
        -----------
        prefix : ProvenanceChain
            The prefix to watch. Must be a tuple representing a part of a task's provenance chain.

        notifier : TaskWorker
            The object to be notified when the watched prefix is no longer in use.
            Its notify method will be called with the watched prefix as an argument.

        task : Task
            The task associated with this watch operation if it was called from consume_work.

        Returns:
        --------
        bool
            True if the notifier was successfully added to the watch list for the given prefix.
            False if the notifier was already in the watch list for this prefix.

        Raises:
        -------
        ValueError
            If the provided prefix is not a tuple.
        """
        if not isinstance(prefix, tuple):
            raise ValueError("Prefix must be a tuple")

        added = False
        with self.notifiers_lock:
            if notifier not in self.notifiers[prefix]:
                self.notifiers[prefix].append(notifier)
                added = True

        if task is not None:
            should_notify = False
            with self.provenance_lock:
                if self.provenance.get(prefix, 0) == 0:
                    should_notify = True

            if should_notify:
                self._notify_task_completion(prefix, task)

        return added

    def unwatch(self, prefix: ProvenanceChain, notifier: TaskWorker) -> bool:
        if not isinstance(prefix, tuple):
            raise ValueError("Prefix must be a tuple")
        with self.notifiers_lock:
            if prefix in self.notifiers and notifier in self.notifiers[prefix]:
                self.notifiers[prefix].remove(notifier)
                if not self.notifiers[prefix]:
                    del self.notifiers[prefix]
                return True
        return False

    def _notify_task_completion(self, prefix: tuple, task: Task):
        to_notify = []
        with self.notifiers_lock:
            for notifier in self.notifiers[prefix]:
                to_notify.append((notifier, prefix))

        for notifier, prefix in to_notify:
            with self.task_lock:
                self.active_tasks += 1

            # Use a named function instead of a lambda to avoid closure issues
            def task_completed_callback(future, worker=notifier, task=task):
                self._task_completed(worker, task, future)

            future = self.graph._thread_pool.submit(notifier.notify, prefix)
            future.add_done_callback(task_completed_callback)

    def _dispatch_once(self) -> bool:
        try:
            worker, task = self.work_queue.get(timeout=1)
            with self.task_lock:
                self.active_tasks += 1
            future = self.graph._thread_pool.submit(self._execute_task, worker, task)

            # Use a named function instead of a lambda to avoid closure issues
            def task_completed_callback(future, worker=worker, task=task):
                self._task_completed(worker, task, future)

            future.add_done_callback(task_completed_callback)
            return True

        except Empty:
            return False

    def dispatch(self):
        while True:
            # making sure that we can access active_tasks in a thread-safe way
            with self.task_lock:
                if (
                    self.stop_event.is_set()
                    and self.work_queue.empty()
                    and self.active_tasks == 0
                ):
                    break
            self._dispatch_once()

    def _execute_task(self, worker: TaskWorker, task: Task):
        task_id = self._get_next_task_id()
        with self.task_lock:
            self.debug_active_tasks[task_id] = (worker, task)

        try:
            worker._pre_consume_work(task)
        except Exception:
            raise  # Re-raise the caught exception
        finally:
            with self.task_lock:
                if task_id in self.debug_active_tasks:
                    del self.debug_active_tasks[task_id]

    def _get_next_task_id(self) -> int:
        with self.task_lock:
            self.task_id_counter += 1
            return self.task_id_counter

    def _task_to_dict(self, worker: TaskWorker, task: Task, error: str = "") -> Dict:
        data = {
            "id": self._get_task_id(task),
            "type": type(task).__name__,
            "worker": worker.name,
            "provenance": [f"{worker}_{id}" for worker, id in task._provenance],
            "input_provenance": [
                {input_task.name: input_task.model_dump()}
                for input_task in task._input_provenance
            ],
        }
        if error:
            data["error"] = error
        return data

    def get_queued_tasks(self) -> List[Dict]:
        return [
            self._task_to_dict(worker, task) for worker, task in self.work_queue.queue
        ]

    def get_active_tasks(self) -> List[Dict]:
        with self.task_lock:
            return [
                self._task_to_dict(worker, task)
                for task_id, (worker, task) in self.debug_active_tasks.items()
            ]

    def get_completed_tasks(self) -> List[Dict]:
        with self.task_lock:
            return [
                self._task_to_dict(worker, task)
                for worker, task in self.completed_tasks
            ]

    def get_failed_tasks(self) -> List[Dict]:
        with self.task_lock:
            return [
                self._task_to_dict(worker, task, error)
                for worker, task, error in self.failed_tasks
            ]

    def _get_task_id(self, task: Task) -> str:
        # Use the last entry in the _provenance list as the task ID
        if task._provenance:
            return f"{task._provenance[-1][0]}_{task._provenance[-1][1]}"
        else:
            # Fallback in case _provenance is empty
            return f"unknown_{id(task)}"

    def _task_completed(self, worker: TaskWorker, task: Task, future):
        success: bool = False
        error_message: str = ""
        try:
            # This will raise an exception if the task failed
            _ = future.result()

            # Handle successful task completion
            logging.info(f"Task {task.name} completed successfully")
            success = True

        except Exception as e:
            # Handle task failure
            error_message = str(e)
            logging.exception(f"Task {task.name} failed with exception: {str(e)}")

            # Anything else that needs to be done when a task fails?

        finally:
            # This code will run whether the task succeeded or failed

            # Determine whether we should retry the task
            if not success:
                if worker.num_retries > 0:
                    if task.retry_count < worker.num_retries:
                        task.increment_retry_count()
                        with self.task_lock:
                            self.active_tasks -= 1
                            self.work_queue.put((worker, task))
                        logging.info(
                            f"Retrying task {task.name} for the {task.retry_count} time"
                        )
                        return

                with self.task_lock:
                    self.failed_tasks.appendleft((worker, task, error_message))
                    self.total_failed_tasks += 1
                logging.error(
                    f"Task {task.name} failed after {task.retry_count} retries"
                )
                # we'll fall through and do the clean up
            else:
                with self.task_lock:
                    self.completed_tasks.appendleft((worker, task))
                    self.total_completed_tasks += 1

            self._remove_provenance(task)
            with self.task_lock:
                self.active_tasks -= 1
                if self.active_tasks == 0 and self.work_queue.empty():
                    self.task_completion_event.set()

    def add_work(self, worker: TaskWorker, task: Task):
        self._add_provenance(task)
        self.work_queue.put((worker, task))

    def add_multiple_work(self, work_items: List[Tuple[TaskWorker, Task]]):
        # the ordering of adding provenance first is important for join tasks to
        # work correctly. Otherwise, caching may lead to fast execution of tasks
        # before all the provenance is added.
        for worker, task in work_items:
            self._add_provenance(task)
        for item in work_items:
            self.work_queue.put(item)

    def stop(self):
        self.stop_event.set()

    def wait_for_completion(self, wait_for_quit=False):
        self.task_completion_event.wait()

        if wait_for_quit:
            while not is_quit_requested():
                # Sleep for a short time to avoid busy waiting
                time.sleep(0.1)

    def start_web_interface(self):
        web_thread = threading.Thread(
            target=run_web_interface, args=(self, self.web_port)
        )
        web_thread.daemon = (
            True  # This ensures the web thread will exit when the main thread exits
        )
        web_thread.start()
