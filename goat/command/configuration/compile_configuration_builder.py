from __future__ import annotations
from pathlib import Path
from typing import Iterable
from goat.command.configuration.compile_configuration import CompileConfiguration


class CompileConfigurationBuilder:
    compile_configuration: CompileConfiguration

    def __init__(
        self,
        executable: str | Path,
        source_file: Path,
        object_file: Path,
    ) -> None:
        self.compile_configuration = CompileConfiguration(
            executable,
            source_file,
            object_file,
        )

    def add_include_path(self, include_path: Path) -> CompileConfigurationBuilder:
        self.compile_configuration.include_paths.append(include_path)
        return self

    def add_include_paths(
        self,
        include_path: Iterable[Path],
    ) -> CompileConfigurationBuilder:
        self.compile_configuration.include_paths.extend(include_path)
        return self

    def add_define(self, define: str) -> CompileConfigurationBuilder:
        self.compile_configuration.defines.append(define)
        return self

    def add_defines(self, defines: Iterable[str]) -> CompileConfigurationBuilder:
        self.compile_configuration.defines.extend(defines)
        return self

    def add_flag(self, flag: str) -> CompileConfigurationBuilder:
        self.compile_configuration.flags.append(flag)
        return self

    def add_flags(self, flags: Iterable[str]) -> CompileConfigurationBuilder:
        self.compile_configuration.flags.extend(flags)
        return self

    def build(self) -> CompileConfiguration:
        return self.compile_configuration
