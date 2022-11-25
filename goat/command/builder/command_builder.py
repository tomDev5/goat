from abc import ABC, abstractmethod
from goat.command.builder.command import Command
from goat.command.configuration.compile_configuration import CompileConfiguration
from goat.command.configuration.link_configuration import LinkConfiguration


class CommandBuilder(ABC):
    @classmethod
    @abstractmethod
    def build_compile(cls, compile_configuration: CompileConfiguration) -> Command:
        ...

    @classmethod
    @abstractmethod
    def build_link(cls, link_configuration: LinkConfiguration) -> Command:
        ...
