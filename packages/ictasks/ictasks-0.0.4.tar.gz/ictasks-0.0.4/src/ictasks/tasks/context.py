"""
This module has the context a task is run in
"""

from pathlib import Path

from ictasks.stopping_condition import StoppingCondition
from ictasks.worker import Worker
from .task import Task


class TaskContext:
    """
    The context a task is run in
    """

    def __init__(
        self,
        work_dir: Path,
        launch_wrapper,
        worker: Worker,
        task: Task,
        cores_per_task: int,
        job_id: str,
        stopping_condition: StoppingCondition,
    ) -> None:
        self.work_dir = work_dir
        self.launch_wrapper = launch_wrapper
        self.worker = worker
        self.task = task
        self.cores_per_task = cores_per_task
        self.job_id = job_id
        self.full_cmd = ""

        task_label = f"{self.worker.host}-id{self.worker.worker_id}-{self.job_id}"
        task_file_name = f"task-{task_label}.{self.task.task_id}"
        self.task_file_path = self.work_dir / Path(task_file_name)

        self.stopping_condition = stopping_condition
        self.stopping_condition.set_path(self.task_file_path)
        self.pid = None
        self.popen_ctx = None

    def poll(self):
        return self.popen_ctx.poll()

    def check_magic(self) -> bool:
        with open(self.get_stop_path(), "r", encoding="utf-8") as f:
            for line in f:
                if self.stopping_condition.stopmagic in line:
                    return True
        return False

    def get_stop_path(self):
        return self.task_file_path / self.stopping_condition.stopfile

    def check_user_exit(self):
        self.stopping_condition.eval()
