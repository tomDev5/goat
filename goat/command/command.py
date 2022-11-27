from dataclasses import dataclass
from pathlib import Path


@dataclass
class Command:
    executable: str | Path
    parameters: list[str | Path]
    env: dict[str, str] | None

    def to_list(self) -> list[str]:
        return list(map(str, (self.executable, *self.parameters)))

    def env_dict(self) -> dict[str, str]:
        if (self.env is None):
            return {}
        return self.env

    def to_string(self) -> str:
        return " ".join(self.to_list())
