from dataclasses import dataclass
from pathlib import Path


@dataclass
class Command:
    executable: str | Path
    parameters: list[str | Path]

    def to_list(self) -> list[str]:
        return list(map(str, (self.executable, *self.parameters)))

    def to_string(self) -> str:
        return " ".join(self.to_list())
