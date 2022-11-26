from abc import ABC, abstractmethod
from goat.command.command import Command
from goat.command.build_command.parameters.compile_parameters import CompileParameters
from goat.command.build_command.parameters.link_parameters import LinkParameters


class BaseBuildCommandFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_compile(compile_parameters: CompileParameters) -> Command:
        ...

    @staticmethod
    @abstractmethod
    def create_link(link_parameters: LinkParameters) -> Command:
        ...
