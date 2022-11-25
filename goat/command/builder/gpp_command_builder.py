from pathlib import Path
from goat.command.builder.command_builder import CommandBuilder
from goat.command.configuration.compile_configuration import CompileConfiguration
from goat.command.configuration.link_configuration import LinkConfiguration


class GPPCommandBuilder(CommandBuilder):
    @classmethod
    def build_compile(cls, compile_configuration: CompileConfiguration):
        result: list[str | Path] = []

        result.append(compile_configuration.executable)
        result.extend(
            f"-I{include_path}" for include_path in compile_configuration.include_paths
        )
        result.extend(f"-D{define}" for define in compile_configuration.defines)
        result.extend(compile_configuration.flags)
        result.extend(
            (
                "-c",
                "-o",
                compile_configuration.object_file,
                compile_configuration.source_file,
            )
        )

        return cls.stringify_list(result)

    @classmethod
    def build_link(cls, link_configuration: LinkConfiguration):
        result: list[str | Path] = []

        result.append(link_configuration.executable)
        result.extend(link_configuration.object_files)
        result.extend(
            f"-L{library_path}" for library_path in link_configuration.library_paths
        )
        result.extend(f"-l{library}" for library in link_configuration.libraries)
        result.extend(link_configuration.flags)
        result.extend(("-o", link_configuration.target_file))

        return cls.stringify_list(result)
