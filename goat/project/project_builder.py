from itertools import chain
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
    def link_target_file(
        cls,
        configuration: ProjectConfiguration,
        object_files: list[Path],
        test: bool,
    ) -> CompletedProcess:
        linker_flags = cls.linker_flags(configuration, test)
        object_files_str = list(map(str, object_files))

        return run([configuration.compiler, *object_files_str, *linker_flags])

    @classmethod
    def get_source_object_mapping(
        cls,
        configuration: ProjectConfiguration,
        test: bool = False,
    ) -> dict[Path, Path]:
        binary_source_files = configuration.source_directory.glob("**/*.cc")
        test_source_files = configuration.test_directory.glob("**/*.cc")
        source_files = (
            chain(binary_source_files, test_source_files)
            if test
            else binary_source_files
        )

        source_object_mapping: dict[Path, Path] = {}

        for source_file in source_files:
            relative_source_file = source_file.relative_to(configuration.root_path)

            object_file = (
                configuration.object_directory
                / relative_source_file.parent
                / f"{relative_source_file.name}.o"
            )

            source_object_mapping[source_file] = object_file

        return source_object_mapping

    @classmethod
    def build_target_file(
        cls,
        configuration: ProjectConfiguration,
        test: bool = False,
    ) -> None:
        configuration.build_directory.mkdir(parents=True, exist_ok=True)
        configuration.object_directory.mkdir(parents=True, exist_ok=True)
        configuration.binary_directory.mkdir(parents=True, exist_ok=True)

        source_object_mapping = cls.get_source_object_mapping(configuration, test)

        for source_file, object_file in source_object_mapping.items():
            print(f"Compiling {source_file}")
            object_file.parent.mkdir(parents=True, exist_ok=True)
            result = cls.compile_object_file(
                configuration,
                source_file,
                object_file,
                test,
            )

            if result.returncode != 0:
                print(result.stderr)
                return

        print(f"Linking {configuration.target_file(test)}")

        result = cls.link_target_file(
            configuration,
            list(source_object_mapping.values()),
            test,
        )

        if result.returncode != 0:
            print(result.stderr)
            return
