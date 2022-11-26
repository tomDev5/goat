from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from goat.project.configuration.schema.configuration_schema import ConfigurationSchema
from toml import loads as toml_to_dict
from goat.project.configuration.project_configuration_variant import (
    ProjectConfigurationVariant,
)
from goat.project.build_mode import BuildMode
from goat.project.configuration.project_configuration_variant_factory import (
    ProjectConfigurationVariantFactory,
)
from goat.project.project_path_resolver import ProjectPathResolver


@dataclass
class ProjectConfiguration:
    path_resolver: ProjectPathResolver
    release_configuration: ProjectConfigurationVariant
    debug_configuration: ProjectConfigurationVariant
    test_configuration: ProjectConfigurationVariant

    CONFIGURATION_FILE_NAME = "goat.toml"
    SOURCE_DIRECTORY_NAME = "source"
    INCLUDE_DIRECTORY_NAME = "include"
    TEST_DIRECTORY_NAME = "test"
    BUILD_DIRECTORY_NAME = "build"
    OBJECT_DIRECTORY_NAME = "object"
    BINARY_DIRECTORY_NAME = "binary"

    @classmethod
    def from_path(
        cls,
        root_path: Path,
        configuration_path: Path,
    ) -> ProjectConfiguration:
        configuration_dict = toml_to_dict(configuration_path.read_text())
        return cls.from_configuration(
            ProjectPathResolver(root_path),
            ConfigurationSchema.parse_obj(configuration_dict),
        )

    @classmethod
    def from_configuration(
        cls,
        path_resolver: ProjectPathResolver,
        configuration_schema: ConfigurationSchema,
    ) -> ProjectConfiguration:
        release = ProjectConfigurationVariantFactory.create(
            configuration_schema,
            BuildMode.RELEASE,
        )

        debug = ProjectConfigurationVariantFactory.create(
            configuration_schema,
            BuildMode.DEBUG,
        )

        test = ProjectConfigurationVariantFactory.create(
            configuration_schema,
            BuildMode.TEST,
        )

        return cls(path_resolver, release, debug, test)

    def __init__(
        self,
        path_resolver: ProjectPathResolver,
        release_configuration: ProjectConfigurationVariant,
        debug_configuration: ProjectConfigurationVariant,
        test_configuration: ProjectConfigurationVariant,
    ) -> None:
        self.path_resolver = path_resolver
        self.release_configuration = release_configuration
        self.debug_configuration = debug_configuration
        self.test_configuration = test_configuration

    def configuration_variant(
        self,
        build_mode: BuildMode,
    ) -> ProjectConfigurationVariant:
        match build_mode:
            case BuildMode.RELEASE:
                return self.release_configuration

            case BuildMode.DEBUG:
                return self.debug_configuration

            case BuildMode.TEST:
                return self.test_configuration

    def target(self, build_mode: BuildMode) -> Path:
        name = self.configuration_variant(build_mode).target
        return self.path_resolver.binary_directory(build_mode) / name

    def compiler(self, build_mode: BuildMode) -> str:
        return self.configuration_variant(build_mode).compiler

    def include_paths(self, build_mode: BuildMode) -> list[Path]:
        return self.configuration_variant(build_mode).include_paths

    def compiler_flags(self, build_mode: BuildMode) -> list[str]:
        return self.configuration_variant(build_mode).compiler_flags

    def defines(self, build_mode: BuildMode) -> list[str]:
        return self.configuration_variant(build_mode).defines

    def linker(self, build_mode: BuildMode) -> str:
        return self.configuration_variant(build_mode).linker

    def linker_flags(self, build_mode: BuildMode) -> list[str]:
        return self.configuration_variant(build_mode).linker_flags

    def library_paths(self, build_mode: BuildMode) -> list[Path]:
        return self.configuration_variant(build_mode).library_paths

    def libraries(self, build_mode: BuildMode) -> list[str]:
        return self.configuration_variant(build_mode).libraries
