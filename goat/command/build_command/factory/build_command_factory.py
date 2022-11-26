from goat.command.build_command.factory.toolchain_command_factory import (
    ToolchainCommandFactory,
)
from goat.command.build_command.factory.gpp_command_factory import (
    GPPCommandFactory,
)
from goat.command.build_command.parameters.compile_parameters import CompileParameters
from goat.command.build_command.parameters.link_parameters import LinkParameters
from goat.command.command import Command


class BuildCommandFactory:
    @staticmethod
    def create_toolchain_factory(program: str) -> type[ToolchainCommandFactory]:
        match program:
            case "g++":
                return GPPCommandFactory

        raise NotImplementedError()

    @classmethod
    def create_compile(
        cls,
        program: str,
        compile_parameters: CompileParameters,
    ) -> Command:
        return cls.create_toolchain_factory(program).create_compile(compile_parameters)

    @classmethod
    def create_link(cls, program: str, link_parameters: LinkParameters) -> Command:
        return cls.create_toolchain_factory(program).create_link(link_parameters)
