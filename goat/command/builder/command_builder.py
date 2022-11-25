from abc import ABC, abstractmethod
from goat.command.builder.command import Command
from goat.command.configuration.compile_configuration import CompileConfiguration
from goat.command.configuration.link_configuration import LinkConfiguration


class CommandBuilder(ABC):
    @staticmethod
    @abstractmethod
    def build_compile(compile_configuration: CompileConfiguration) -> Command:
        ...

    @staticmethod
    @abstractmethod
    def build_link(link_configuration: LinkConfiguration) -> Command:
        ...
