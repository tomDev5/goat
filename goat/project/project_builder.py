from pathlib import Path
from subprocess import CompletedProcess, run
from goat.project.project_configuration import ProjectConfiguration


class ProjectBuilder:
    @staticmethod
    def include_flags(configuration: ProjectConfiguration) -> list[str]:
        return [
            f"-I{include_path}"
            for include_path in (
                configuration.include_paths + [configuration.include_directory]
            )
        ]

    @staticmethod
    def compiler_flags(
        configuration: ProjectConfiguration,
        object_file: Path,
    ) -> list[str]:
        return configuration.compiler_flags + [
            "-c",
            "-o",
            str(object_file),
        ]

    @staticmethod
    def linker_flags(
        configuration: ProjectConfiguration,
        binary_file: Path,
    ) -> list[str]:
        return ["-o", str(binary_file)]

    @classmethod
    def compile_object_file(
        cls,
        configuration: ProjectConfiguration,
        source_file: Path,
        object_file: Path,
    ) -> CompletedProcess:
        include_flags = cls.include_flags(configuration)
        compiler_flags = cls.compiler_flags(configuration, object_file)

        return run(
            [
                configuration.compiler,
                *include_flags,
                *compiler_flags,
                str(source_file),
            ]
        )

    @classmethod
    def link_binary_file(
        cls,
        configuration: ProjectConfiguration,
        object_files: list[Path],
        binary_file: Path,
    ) -> CompletedProcess:
        linker_flags = cls.linker_flags(configuration, binary_file)
        object_files_str = list(map(str, object_files))

        return run([configuration.compiler, *linker_flags, *object_files_str])
