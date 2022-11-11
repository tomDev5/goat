from pathlib import Path
from enum import Enum

TEMPLATE_DIRECTORY = Path(__file__).parent / "templates"


class Template(Enum):
    MAIN = "main"
    TEST = "test"

    def read(self) -> str:
        return (TEMPLATE_DIRECTORY / f"{self.value}.template").read_text()
