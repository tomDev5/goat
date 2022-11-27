from pathlib import Path
from goat.command.command import Command
from goat.command.build_command.factory.toolchain_command_factory import (
    ToolchainCommandFactory,
)
from goat.command.build_command.parameters.compile_parameters import CompileParameters
from goat.command.build_command.parameters.link_parameters import LinkParameters


class GPPCommandFactory(ToolchainCommandFactory):
    @staticmethod
    def create_compile(compile_parameters: CompileParameters) -> Command:
        parameters: list[str | Path] = []

        parameters.extend(
            f"-I{include_path}" for include_path in compile_parameters.include_paths
        )
        parameters.extend(f"-D{define}" for define in compile_parameters.defines)
        parameters.extend(compile_parameters.flags)
        parameters.extend(
            (
                "-c",
                "-o",
                compile_parameters.object_file,
                compile_parameters.source_file,
            )
        )

        return Command(compile_parameters.executable, parameters)

    @staticmethod
    def create_link(link_parameters: LinkParameters) -> Command:
        parameters: list[str | Path] = []

        parameters.extend(link_parameters.object_files)
        parameters.extend(
            f"-L{library_path}" for library_path in link_parameters.library_paths
        )
        parameters.extend(f"-l{library}" for library in link_parameters.libraries)
        parameters.extend(link_parameters.flags)
        parameters.extend(("-o", link_parameters.target_file))

        return Command(link_parameters.executable, parameters)