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
    def create_toolchain_factory(toolchain: str) -> type[ToolchainCommandFactory]:
        match toolchain:
            case "g++":
                return GPPCommandFactory

        raise NotImplementedError()

    @classmethod
    def create_compile(
        cls,
        toolchain: str,
        compile_parameters: CompileParameters,
    ) -> Command:
        return cls.create_toolchain_factory(toolchain).create_compile(
            compile_parameters
        )

    @classmethod
    def create_link(cls, toolchain: str, link_parameters: LinkParameters) -> Command:
        return cls.create_toolchain_factory(toolchain).create_link(link_parameters)
