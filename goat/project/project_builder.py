from pathlib import Path
from subprocess import PIPE, CompletedProcess, run

from loguru import logger
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
        test: bool,
    ) -> list[str]:
        test_linker_flags = [f"-l{library}" for library in cls.TEST_LINK_LIBRARIES]
        return (test_linker_flags if test else []) + [
            "-o",
            str(configuration.target_file(test)),
        ]

    @classmethod
    def compile_object_file(
        cls,
        configuration: ProjectConfiguration,
        source_file: Path,
        object_file: Path,
        test: bool = False,
    ) -> None:
        logger.trace(f"Compiling {source_file.relative_to(configuration.root_path)}")

        include_flags = cls.include_flags(configuration)
        compiler_flags = cls.compiler_flags(configuration, object_file, test)
        result = run(
            [configuration.compiler, str(source_file), *include_flags, *compiler_flags],
            stderr=PIPE,
            text=True,
        )
        if result.returncode != 0:
            raise Exception(result.stderr)

    @classmethod
    def link_target_file(
        cls,
        configuration: ProjectConfiguration,
        object_files: list[Path],
        test: bool,
    ) -> None:
        logger.trace(
            f"Linking {configuration.target_file(test).relative_to(configuration.root_path)}"
        )

        linker_flags = cls.linker_flags(configuration, test)
        object_files_str = list(map(str, object_files))
        result = run(
            [configuration.compiler, *object_files_str, *linker_flags],
            stderr=PIPE,
            text=True,
        )
        if result.returncode != 0:
            raise Exception(result.stderr)

    @classmethod
    def get_binary_object_mapping(
        cls,
        configuration: ProjectConfiguration,
    ) -> dict[Path, Path]:
        binary_source_files = list(configuration.source_directory.glob("**/*.cc"))
        return cls.get_object_mapping(configuration, binary_source_files)

    @classmethod
    def get_test_object_mapping(
        cls,
        configuration: ProjectConfiguration,
    ) -> dict[Path, Path]:
        test_source_files = list(configuration.test_directory.glob("**/*.cc"))
        return cls.get_object_mapping(configuration, test_source_files)

    @classmethod
    def get_object_mapping(
        cls,
        configuration: ProjectConfiguration,
        source_files: list[Path],
    ) -> dict[Path, Path]:
        object_mapping: dict[Path, Path] = {}

        for source_file in source_files:
            relative_source_file = source_file.relative_to(configuration.root_path)

            object_file = (
                configuration.object_directory
                / relative_source_file.parent
                / f"{relative_source_file.name}.o"
            )

            object_mapping[source_file] = object_file

        return object_mapping

    @classmethod
    def build_target_file(
        cls,
        configuration: ProjectConfiguration,
        test: bool = False,
    ) -> None:
        configuration.build_directory.mkdir(parents=True, exist_ok=True)
        configuration.object_directory.mkdir(parents=True, exist_ok=True)
        configuration.binary_directory.mkdir(parents=True, exist_ok=True)

        object_mapping = cls.get_binary_object_mapping(configuration)
        if test:
            object_mapping |= cls.get_test_object_mapping(configuration)

        for source_file, object_file in object_mapping.items():
            object_file.parent.mkdir(parents=True, exist_ok=True)
            cls.compile_object_file(
                configuration,
                source_file,
                object_file,
                test,
            )

        cls.link_target_file(
            configuration,
            list(object_mapping.values()),
            test,
        )
