from typing import Literal, overload
from goat.command.command_type import CommandType
from goat.command.compile.compile_command_builder import CompileCommandBuilder
from goat.command.compile.compile_command_builder_factory import (
    CompileCommandBuilderFactory,
)
from goat.command.link.link_command_builder import LinkCommandBuilder
from goat.command.link.link_command_builder_factory import LinkCommandBuilderFactory


class CommandBuilderFactory:
    @overload
    @staticmethod
    def create(
        command_type: Literal[CommandType.COMPILE],
        program: str,
    ) -> CompileCommandBuilder:
        ...

    @overload
    @staticmethod
    def create(
        command_type: Literal[CommandType.LINK],
        program: str,
    ) -> LinkCommandBuilder:
        ...

    @staticmethod
    def create(
        command_type: CommandType,
        program: str,
    ) -> CompileCommandBuilder | LinkCommandBuilder:
        match command_type:
            case CommandType.COMPILE:
                return CompileCommandBuilderFactory.create(program)

            case CommandType.LINK:
                return LinkCommandBuilderFactory.create(program)
