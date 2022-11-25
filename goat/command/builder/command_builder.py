from abc import ABC, abstractmethod
from goat.command.builder.command import Command
from goat.command.parameters.compile_parameters import CompileParameters
from goat.command.parameters.link_parameters import LinkParameters


class CommandBuilder(ABC):
    @staticmethod
    @abstractmethod
    def build_compile(compile_parameters: CompileParameters) -> Command:
        ...

    @staticmethod
    @abstractmethod
    def build_link(link_parameters: LinkParameters) -> Command:
        ...
