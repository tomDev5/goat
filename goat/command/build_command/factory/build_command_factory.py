from goat.command.build_command.factory.base_build_command_factory import (
    BaseBuildCommandFactory,
)
from goat.command.build_command.factory.gpp_build_command_factory import (
    GPPBuildCommandFactory,
)
from goat.command.build_command.parameters.compile_parameters import CompileParameters
from goat.command.build_command.parameters.link_parameters import LinkParameters
from goat.command.command import Command


class BuildCommandFactory:
    @staticmethod
    def get_specific_factory(program: str) -> type[BaseBuildCommandFactory]:
        match program:
            case "g++":
                return GPPBuildCommandFactory

        raise NotImplementedError()

    @classmethod
    def create_compile(
        cls,
        program: str,
        compile_parameters: CompileParameters,
    ) -> Command:
        return cls.get_specific_factory(program).create_compile(compile_parameters)

    @classmethod
    def create_link(cls, program: str, link_parameters: LinkParameters) -> Command:
        return cls.get_specific_factory(program).create_link(link_parameters)
