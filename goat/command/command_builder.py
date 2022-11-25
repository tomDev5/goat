from abc import ABC, abstractmethod
from pathlib import Path
from typing import TypeVar

T = TypeVar("T", bound="CommandBuilder")


class CommandBuilder(ABC):
    executable: str | Path

    def __init__(self, executable: str | Path) -> None:
        self.executable = executable

    @abstractmethod
    def build_list(self) -> list[str | Path]:
        ...

    def build(self) -> list[str]:
        return list(map(str, self.build_list()))
