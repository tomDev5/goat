from __future__ import annotations
from pathlib import Path
from typing import Iterable
from goat.command.parameters.compile_parameters import CompileParameters


class CompileParametersBuilder:
    compile_parameters: CompileParameters

    def __init__(
        self,
        executable: str | Path,
        source_file: Path,
        object_file: Path,
    ) -> None:
        self.compile_parameters = CompileParameters(
            executable,
            source_file,
            object_file,
        )

    def add_include_path(self, include_path: Path) -> CompileParametersBuilder:
        self.compile_parameters.include_paths.append(include_path)
        return self

    def add_include_paths(
        self,
        include_path: Iterable[Path],
    ) -> CompileParametersBuilder:
        self.compile_parameters.include_paths.extend(include_path)
        return self

    def add_define(self, define: str) -> CompileParametersBuilder:
        self.compile_parameters.defines.append(define)
        return self

    def add_defines(self, defines: Iterable[str]) -> CompileParametersBuilder:
        self.compile_parameters.defines.extend(defines)
        return self

    def add_flag(self, flag: str) -> CompileParametersBuilder:
        self.compile_parameters.flags.append(flag)
        return self

    def add_flags(self, flags: Iterable[str]) -> CompileParametersBuilder:
        self.compile_parameters.flags.extend(flags)
        return self

    def build(self) -> CompileParameters:
        return self.compile_parameters
