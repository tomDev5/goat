from pathlib import Path
from subprocess import CompletedProcess, run
from goat.project.project_configuration import ProjectConfiguration


class ProjectBuilder:

    TEST_MACROS = ["TEST"]
    TEST_LINK_LIBRARIES = ["gtest", "gtest_main", "pthread"]

    @staticmethod
    def include_flags(configuration: ProjectConfiguration) -> list[str]:
        return [
            f"-I{include_path}"
            for include_path in (
                configuration.include_paths + [configuration.include_directory]
            )
        ]

    @classmethod
    def compiler_flags(
        cls,
        configuration: ProjectConfiguration,
        object_file: Path,
        test: bool = False,
    ) -> list[str]:
        test_compiler_flags = [f"-D{macro}" for macro in cls.TEST_MACROS]

        return (
            (test_compiler_flags if test else [])
            + configuration.compiler_flags
            + [
                "-c",
                "-o",
                str(object_file),
            ]
        )

    @classmethod
    def linker_flags(
        cls,
        configuration: ProjectConfiguration,
        binary_file: Path,
        test: bool,
    ) -> list[str]:
        test_linker_flags = [f"-l{library}" for library in cls.TEST_LINK_LIBRARIES]
        return (test_linker_flags if test else []) + ["-o", str(binary_file)]

    @classmethod
    def compile_object_file(
        cls,
        configuration: ProjectConfiguration,
        source_file: Path,
        object_file: Path,
        test: bool = False,
    ) -> CompletedProcess:
        include_flags = cls.include_flags(configuration)
        compiler_flags = cls.compiler_flags(configuration, object_file, test)

        return run(
            [
                configuration.compiler,
                str(source_file),
                *include_flags,
                *compiler_flags,
            ]
        )

    @classmethod
    def link_binary_file(
        cls,
        configuration: ProjectConfiguration,
        object_files: list[Path],
        binary_file: Path,
        test: bool,
    ) -> CompletedProcess:
        linker_flags = cls.linker_flags(configuration, binary_file, test)
        object_files_str = list(map(str, object_files))

        return run([configuration.compiler, *object_files_str, *linker_flags])
