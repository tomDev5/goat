from pathlib import Path
from typing import Any, Literal, overload
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
        compiler_or_linker: str,
        executable: str | Path,
        source_file: Path,
        object_file: Path,
    ) -> CompileCommandBuilder:
        ...

    @overload
    @staticmethod
    def create(
        command_type: Literal[CommandType.LINK],
        compiler_or_linker: str,
        executable: str | Path,
        target_file: Path,
        object_files: list[Path],
    ) -> LinkCommandBuilder:
        ...

    @staticmethod  # type: ignore[misc]
    def create(
        command_type: CommandType,
        compiler_or_linker: str,
        *arguments: Any,
    ) -> CompileCommandBuilder | LinkCommandBuilder:
        match command_type:
            case CommandType.COMPILE:
                return CompileCommandBuilderFactory.create(
                    compiler_or_linker,
                    *arguments,
                )

            case CommandType.LINK:
                return LinkCommandBuilderFactory.create(
                    compiler_or_linker,
                    *arguments,
                )
