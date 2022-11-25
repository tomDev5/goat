from pathlib import Path
from goat.command.builder.command import Command
from goat.command.builder.command_builder import CommandBuilder
from goat.command.configuration.compile_configuration import CompileConfiguration
from goat.command.configuration.link_configuration import LinkConfiguration


class GPPCommandBuilder(CommandBuilder):
    @classmethod
    def build_compile(cls, compile_configuration: CompileConfiguration) -> Command:
        parameters: list[str | Path] = []

        parameters.extend(
            f"-I{include_path}" for include_path in compile_configuration.include_paths
        )
        parameters.extend(f"-D{define}" for define in compile_configuration.defines)
        parameters.extend(compile_configuration.flags)
        parameters.extend(
            (
                "-c",
                "-o",
                compile_configuration.object_file,
                compile_configuration.source_file,
            )
        )

        return Command(compile_configuration.executable, parameters)

    @classmethod
    def build_link(cls, link_configuration: LinkConfiguration) -> Command:
        parameters: list[str | Path] = []

        parameters.extend(link_configuration.object_files)
        parameters.extend(
            f"-L{library_path}" for library_path in link_configuration.library_paths
        )
        parameters.extend(f"-l{library}" for library in link_configuration.libraries)
        parameters.extend(link_configuration.flags)
        parameters.extend(("-o", link_configuration.target_file))

        return Command(link_configuration.executable, parameters)
