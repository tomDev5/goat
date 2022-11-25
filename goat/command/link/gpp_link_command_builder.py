from pathlib import Path
from goat.command.link.link_command_builder import LinkCommandBuilder


class GPPLinkCommandBuilder(LinkCommandBuilder):
    def build_list(self) -> list[str | Path]:
        result: list[str | Path] = []

        result.append(self.executable)
        result.extend(self.object_files)
        result.extend(f"-L{library_path}" for library_path in self.library_paths)
        result.extend(f"-l{library}" for library in self.libraries)
        result.extend(self.flags)
        result.extend(("-o", self.target_file))

        return result
