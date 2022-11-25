from abc import ABC, abstractmethod
from pathlib import Path

from goat.command.configuration.compile_configuration import CompileConfiguration
from goat.command.configuration.link_configuration import LinkConfiguration


class CommandBuilder(ABC):
    @staticmethod
    def stringify_list(string_or_path_list: list[str | Path]) -> list[str]:
        return list(map(str, string_or_path_list))

    @classmethod
    @abstractmethod
    def build_compile(cls, compile_configuration: CompileConfiguration) -> list[str]:
        ...

    @classmethod
    @abstractmethod
    def build_link(cls, link_configuration: LinkConfiguration) -> list[str]:
        ...
