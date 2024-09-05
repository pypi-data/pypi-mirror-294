"""
This module is for a single batch job or session
"""

import os
import time
import logging

from .environment import Environment
from .tasks import TaskCollection, TaskContext, TaskLauncher
from .stopping_condition import StoppingCondition

from .utils.queue import Queue

logger = logging.getLogger(__name__)


class Session:
    """This class represents a single batch job or session

    Attributes:
        job_id (str): Idenitifier for the job or session
        nodelist (:obj:`list`): List of compute nodes available to run on
        tasks_path (:obj:`Path`): Path to a list of tasks to run
    """

    def __init__(
        self,
        environment: Environment,
        tasks: TaskCollection,
        launcher: TaskLauncher,
        sleep_duration: int = 100,
        keep_finished_tasks: bool = False,
    ) -> None:

        self.env = environment
        self.tasks = tasks
        self.launcher = launcher

        self.sleep = sleep_duration
        self.keep = keep_finished_tasks

        self.worker_queue = Queue()
        self.running_tasks: dict = {}

    def run(self):
        """
        Run the session by iterating over all
        tasks an assigning them to waiting workers.
        """
        logger.info("Start processing tasks")

        if not self.worker_queue:
            for worker in self.workers:
                self.worker_queue.push(worker.id)

        self._log_launch_info()

        for task in self.tasks:
            if self.worker_queue.available():
                self._launch(task)
            else:
                worker_id = self._wait_on_task()
                self.worker_queue.push(worker_id)

        while self.running_tasks:
            self._wait_on_task()
        logger.info("All tasks completed.")

    def run_sequential(self):

        for task in self.tasks:
            task_dir = task.work_dir / task.task_id
            os.makedirs(task_dir, exist_ok=True)
            task.write(task_dir)

        for task in self.tasks:
            logger.debug("Launching task: %s", task.launch_cmd)

            t1 = time.time()
            proc = self.launcher.launch(task)
            walltime = time.time() - t1

            self.launcher.on_task_completed(task, proc, walltime)

    def _log_launch_info(self):
        num_workers = len(self.env.workers)
        num_tasks = len(self.tasks)

        ppn = self.env.workers.processes_per_node
        logger.info("Started with %d workers (%d per node).", num_workers, ppn)
        if self.tasks.has_grouped_tasks():
            grouped_tasks = self.tasks.num_grouped_tasks
            logger.info(
                "Has %d tasks, grouped as %d metatasks.",
                num_tasks,
                grouped_tasks,
            )
        else:
            logger.info("Has %d tasks.", num_tasks)

        if num_tasks % num_workers != 0:
            logger.warning(
                "Number of %d tasks should be multiple of %d workers.",
                num_tasks,
                num_workers,
            )
        if num_tasks / num_workers > 20:
            msg = f"""There are {num_tasks} tasks for {num_workers} workers.
                This tool is not ideal for high-throughput workloads.
                You can aggregate tasks using export TASKFARM_GROUP=xxx
                with xxx how many consecutive tasks to group in a metatask"""
            logger.warning(msg)

    def _launch(self, task):
        worker = self.env.workers[self.worker_queue.pop()]

        stopping_condition = StoppingCondition()

        task_ctx = TaskContext(
            self.tasks.work_dir,
            self.launcher.launch_wrapper,
            worker,
            task,
            self.launcher.cores_per_task,
            self.env.job_id,
            stopping_condition,
        )
        task_ctx = self.launcher.launch(task_ctx)

        self.running_tasks[task_ctx.pid] = task_ctx

    def _wait_on_task(self):
        finished = {}
        while True:
            for pid, task_ctx in self.running_tasks.items():
                if task_ctx.poll() is not None:
                    finished[pid] = {"status": task_ctx.poll()}
                task_ctx.check_user_exit()

            if len(finished) > 0:
                first_pid = list(finished.keys())[0]
                should_exit = signal = finished[first_pid]["status"]
                break
            time.sleep(self.sleep)

        worker_id = self.running_tasks[first_pid].worker.id
        if should_exit != 0:
            task_cmd = self.running_tasks[first_pid].task.launch_cmd
            logger.error("'%s' killed by sig %d", task_cmd, signal)

        if not self.keep:
            os.unlink(self.running_tasks[first_pid].task_file_path)
            del self.running_tasks[first_pid]
        return worker_id
