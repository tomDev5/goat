from __future__ import annotations
from pathlib import Path
from typing import Iterable
from goat.command.build_command.parameters.compile_parameters import CompileParameters


class CompileParametersBuilder:
    executable: str | Path
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
        self.executable = executable
        self.source_file = source_file
        self.object_file = object_file
        self.include_paths = []
        self.defines = []
        self.flags = []

    def add_include_path(self, include_path: Path) -> CompileParametersBuilder:
        self.include_paths.append(include_path)
        return self

    def add_include_paths(
        self,
        include_path: Iterable[Path],
    ) -> CompileParametersBuilder:
        self.include_paths.extend(include_path)
        return self

    def add_define(self, define: str) -> CompileParametersBuilder:
        self.defines.append(define)
        return self

    def add_defines(self, defines: Iterable[str]) -> CompileParametersBuilder:
        self.defines.extend(defines)
        return self

    def add_flag(self, flag: str) -> CompileParametersBuilder:
        self.flags.append(flag)
        return self

    def add_flags(self, flags: Iterable[str]) -> CompileParametersBuilder:
        self.flags.extend(flags)
        return self

    def build(self) -> CompileParameters:
        return CompileParameters(
            self.executable,
            self.source_file,
            self.object_file,
            self.include_paths,
            self.defines,
            self.flags,
        )
