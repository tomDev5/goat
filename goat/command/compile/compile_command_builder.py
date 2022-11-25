from __future__ import annotations
from pathlib import Path
from typing import Iterable, TypeVar
from goat.command.command_builder import CommandBuilder

T = TypeVar("T", bound="CompileCommandBuilder")


class CompileCommandBuilder(CommandBuilder):
    source_file: Path
    object_file: Path
    include_paths: list[Path]
    defines: list[str]
    flags: list[str]

    def __init__(
        self,
        executable: str | Path,
        source_file: Path,
        object_file: Path,
    ) -> None:
        super().__init__(executable)
        self.source_file = source_file
        self.object_file = object_file
        self.include_paths = []
        self.defines = []
        self.flags = []

    def add_include_path(self: T, include_path: Path) -> T:
        self.include_paths.append(include_path)
        return self

    def add_include_paths(self: T, include_path: Iterable[Path]) -> T:
        self.include_paths.extend(include_path)
        return self

    def add_define(self: T, define: str) -> T:
        self.defines.append(define)
        return self

    def add_defines(self: T, defines: Iterable[str]) -> T:
        self.defines.extend(defines)
        return self

    def add_flag(self: T, flag: str) -> T:
        self.flags.append(flag)
        return self

    def add_flags(self: T, flags: Iterable[str]) -> T:
        self.flags.extend(flags)
        return self
