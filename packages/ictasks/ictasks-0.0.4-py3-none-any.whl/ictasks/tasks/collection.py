"""
This module is for a collection of tasks
"""

from pathlib import Path

from iccore.serialization import Serializable

from .task import Task
from .taskfarm_file import TaskfarmFile


class TaskCollection(Serializable):
    """
    This is a collection of tasks which can be 'run' over
    a collection of workers
    """

    def __init__(self, work_dir: Path, group_size: int = 1) -> None:
        self.work_dir = work_dir
        self.group_size = group_size

        self.items: list[Task] = []
        self.num_grouped_tasks: int = 0

    def serialize(self):
        return {
            "group_size": self.group_size,
            "num_grouped_tasks": self.num_grouped_tasks,
            "items": [t.serialize() for t in self.items],
        }

    def read_taskfile(self, path: Path):
        taskfile = TaskfarmFile(self.work_dir, self.group_size)
        self.num_grouped_tasks, self.items = taskfile.read(path)

    def load_from_workdir(self):
        ids = set()
        for entry in self.work_dir.iterdir():
            ids.add(entry.stem)

        self.items = [Task(self.work_dir, each_id) for each_id in ids]
        for item in self.items:
            item.read()

    def __iter__(self):
        return self.items.__iter__()

    def __len__(self):
        return len(self.items)
