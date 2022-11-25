from goat.command.builder.command_builder import CommandBuilder
from goat.command.builder.gpp_command_builder import GPPCommandBuilder


class CommandBuilderFactory:
    @staticmethod
    def create(name: str) -> type[CommandBuilder]:
        match name:
            case "g++":
                return GPPCommandBuilder

        raise NotImplementedError()
