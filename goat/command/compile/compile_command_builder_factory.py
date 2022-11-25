from pathlib import Path
from goat.command.compile.compile_command_builder import CompileCommandBuilder
from goat.command.compile.gpp_compile_command_builder import GPPCompileCommandBuilder


class CompileCommandBuilderFactory:
    @staticmethod
    def create(
        compiler: str,
        executable: str | Path,
        source_file: Path,
        object_file: Path,
    ) -> CompileCommandBuilder:
        match compiler:
            case "g++":
                return GPPCompileCommandBuilder(executable, source_file, object_file)

        raise NotImplementedError()
