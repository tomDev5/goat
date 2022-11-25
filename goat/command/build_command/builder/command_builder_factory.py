from goat.command.build_command.builder.command_builder import CommandBuilder
from goat.command.build_command.builder.gpp_command_builder import GPPCommandBuilder


class CommandBuilderFactory:
    @staticmethod
    def create(program: str) -> type[CommandBuilder]:
        match program:
            case "g++":
                return GPPCommandBuilder

        raise NotImplementedError()
