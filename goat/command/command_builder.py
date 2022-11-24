from abc import ABC, abstractmethod
from pathlib import Path
from typing import TypeVar

T = TypeVar("T", bound="CommandBuilder")


class CommandBuilder(ABC):
    program: str | Path

    def __init__(self, program: str | Path) -> None:
        self.program = program

    @abstractmethod
    def build_list(self) -> list[str | Path]:
        ...

    def build(self) -> str:
        return " ".join(map(str, self.build_list()))
