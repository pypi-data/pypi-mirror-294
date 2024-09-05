"""
This module describes a task, i.e. a small unit of work
"""

from pathlib import Path

from iccore.serialization import read_json, write_json, Serializable

from .status import TaskStatus


class Task(Serializable):
    def __init__(
        self, task_id: str = "", launch_cmd: str = "", extra_paths: list | None = None
    ):
        self.launch_cmd = launch_cmd
        self.task_id = task_id
        self.work_dir: Path = Path()
        self.inputs: dict = {}
        if extra_paths:
            self.extra_paths = extra_paths
        else:
            self.extra_paths = []
        self.status = TaskStatus()

    def set_inputs(self, inputs):
        self.inputs = dict(inputs)
        if "command" not in self.inputs:
            self.inputs["command"] = self.launch_cmd

    def serialize(self):
        return {
            "launch_cmd": self.launch_cmd,
            "id": self.task_id,
            "work_dir": self.work_dir,
            "extra_paths": self.extra_paths,
            "inputs": self.inputs,
            "status": self.status.serialize(),
        }

    def deserialize(self, content: dict):
        if "launch_cmd" in content:
            self.launch_cmd = content["launch_cmd"]
        if "id" in content:
            self.task_id = content["id"]
        if "work_dir" in content:
            self.work_dir = content["work_dir"]
        if "inputs" in content:
            self.inputs = content["inputs"]
        if "extra_paths" in content:
            self.extra_paths = content["extra_paths"]
        if "status" in content:
            self.status = TaskStatus()
            self.status.deserialize(content["status"])

    def write(self, path: Path, filename: str = "task.json"):
        write_json(self.serialize(), path / filename)

    def read(self, filename: str = "task.json"):
        content = read_json(self.work_dir / self.task_id / filename)
        self.deserialize(content)
