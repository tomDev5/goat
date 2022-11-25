from pathlib import Path
from goat.command.compile.compile_command_builder import CompileCommandBuilder


class GPPCompileCommandBuilder(CompileCommandBuilder):
    def build_list(self) -> list[str | Path]:
        result: list[str | Path] = []

        result.append(self.executable)
        result.extend(f"-I{include_path}" for include_path in self.include_paths)
        result.extend(f"-D{define}" for define in self.defines)
        result.extend(self.flags)
        result.extend(("-c", "-o", self.object_file, self.source_file))

        return result
