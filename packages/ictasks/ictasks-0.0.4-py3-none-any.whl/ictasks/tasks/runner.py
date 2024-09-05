import logging
import subprocess
from subprocess import Popen
import os

from .task import Task
from .context import TaskContext

logger = logging.getLogger()


class TaskLauncher:
    """
    This class is responsible for launching tasks
    """

    def __init__(
        self,
        launch_wrapper: str = "",
        cores_per_task: int = 1,
        stop_on_error: bool = True,
    ) -> None:
        self.launch_wrapper = launch_wrapper
        self.cores_per_task = cores_per_task
        self.launcher_type: str = ""
        self.runtime_env: str = ""
        self.stop_on_error = stop_on_error

        exclude_params = ["PROFILEREAD", "BASH_FUNC_module()"]
        for param in os.environ:
            if param not in exclude_params:
                export_cmd = f"export {param}='{os.environ[param]}'; "
                self.runtime_env = self.runtime_env + export_cmd

    def launch_task(self, task: Task):

        task_dir = task.work_dir / task.task_id
        stdout_f = open(task_dir / "task_stdout.txt", "w", encoding="utf-8")
        stderr_f = open(task_dir / "task_stderr.txt", "w", encoding="utf-8")

        proc = subprocess.run(
            task.launch_cmd,
            shell=True,
            env=os.environ.copy(),
            cwd=task.work_dir / task.task_id,
            capture_output=True,
            text=True,
            stdout=stdout_f,
            stderr=stderr_f,
            check=self.stop_on_error,
        )
        stdout_f.close()
        stderr_f.close()

        return proc

    def on_task_completed(self, task: Task, proc, walltime: int):

        task.status.walltime = walltime
        task.status.status_code = proc.returncode
        task.write(task.work_dir / task.task_id)

    def write_launch_file(self, task_ctx: TaskContext):
        task_cmd = task_ctx.task.launch_cmd
        wrapped_cmd = f"{self.runtime_env} cd {os.getcwd()} && {task_cmd}"
        with open(task_ctx.task_file_path, "w", encoding="utf-8") as f:
            f.write("#!/bin/bash\n")
            f.write(wrapped_cmd)
        os.chmod(task_ctx.task_file_path, 0o0755)

    def launch(self, task_ctx: TaskContext):
        self.write_launch_file(task_ctx)

        if self.launcher_type == "basic":
            args: list[str] = [str(task_ctx.task_file_path)]
        else:
            args = [
                task_ctx.launch_wrapper,
                "-env",
                "I_MPI_PIN_PROCESSOR_LIST",
                str(task_ctx.worker.cores),
                "-n",
                str(task_ctx.cores_per_task),
                "-host",
                task_ctx.worker.get_host_address(),
                str(task_ctx.task_file_path),
            ]

        task_ctx.full_cmd = ""
        for arg in args:
            task_ctx.full_cmd += arg + " "

        task_ctx.popen_ctx = Popen(args)  # type: ignore
        task_ctx.pid = task_ctx.popen_ctx.pid  # type: ignore
        return task_ctx
