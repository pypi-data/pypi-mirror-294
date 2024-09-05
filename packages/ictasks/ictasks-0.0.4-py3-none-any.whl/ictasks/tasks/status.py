from pathlib import Path

from iccore.serialization import Serializable


def write_file(content, path: Path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


class TaskStatus(Serializable):
    def __init__(self) -> None:
        self.status_code: int = 0
        self.walltime: float = 0.0
        self.stdout: list[str] = []
        self.stderr: str = ""

    def serialize(self) -> dict:
        return {"status_code": self.status_code, "walltime": self.walltime}

    def read_stdout(self, work_dir: Path, task_id: str):
        with open(work_dir / task_id / "task_stdout.txt", "r", encoding="utf-8") as f:
            self.stdout = f.readlines()

    def write_status_code(self, path: Path) -> None:
        write_file(self.status_code, path / "task_status_code.dat")

    def deserialize(self, content: dict) -> None:
        if "status_code" in content:
            self.status_code = content["status_code"]

        if "walltime" in content:
            self.walltime = content["walltime"]
