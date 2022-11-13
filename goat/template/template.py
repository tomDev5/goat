from pathlib import Path
from enum import Enum

TEMPLATE_DIRECTORY = Path(__file__).parent


class Template(Enum):
    CONFIGURATION = "configuration"
    MAIN = "main"
    TEST = "test"

    def read(self) -> str:
        return (TEMPLATE_DIRECTORY / f"{self.value}.template").read_text()
