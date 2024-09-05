"""
This module has stopping conditions for tasks
"""

from pathlib import Path
import sys
import os
import logging

logger = logging.getLogger(__name__)


class StoppingCondition:
    """
    This condition stops processing if a particular file
    is found with a predefined phrase.
    """

    def __init__(self, stopfile: Path | None = None, stopmagic: str = "") -> None:
        self.stopmagic = stopmagic
        self.stopfile = stopfile
        self.path: Path | None = None

    def set_path(self, path: Path):
        if self.stopfile is not None:
            self.path = path / self.stopfile

    def check_magic(self) -> bool:
        """
        Is the magic phrase found in the file?
        """
        if not self.path:
            return False
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                if self.stopmagic in line:
                    return True
        return False

    def eval(self):
        """
        Stop processing if the stop condition is hit
        """

        if not self.path:
            return

        if os.path.exists(self.path) and self.stopmagic == "":
            logger.info("Exit because stop-file %s is present.", self.path)
            sys.exit(1)

        if os.path.exists(self.path) and self.check_magic():
            logger.info(
                "Exit because file %s contains magic %s", self.path, self.stopmagic
            )
            sys.exit(1)
