from pathlib import Path
from goat.command.link.gpp_link_command_builder import GPPLinkCommandBuilder
from goat.command.link.link_command_builder import LinkCommandBuilder


class LinkCommandBuilderFactory:
    @staticmethod
    def create(
        linker: str,
        executable: str | Path,
        target_file: Path,
        object_files: list[Path],
    ) -> LinkCommandBuilder:
        match linker:
            case "g++":
                return GPPLinkCommandBuilder(executable, target_file, object_files)

        raise NotImplementedError()
