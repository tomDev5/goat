from datetime import datetime
from pathlib import Path
from goat.project.build_mode import BuildMode
from goat.project.configuration.project_configuration import ProjectConfiguration
from goat.project.project_path_resolver import ProjectPathResolver
from goat.project.changes.file_timestamps import FileTimestamps
from goat.project.changes.project_timestamps import ProjectTimestamps


class ProjectTimestampsFactory:
    @classmethod
    def create(
        cls,
        project_configuration: ProjectConfiguration,
        build_mode: BuildMode,
    ) -> ProjectTimestamps:
        files_timestamps = cls.create_files_timestamps(
            project_configuration.path_resolver,
            build_mode,
        )

        target_file_time = cls.get_target_file_time(project_configuration, build_mode)

        latest_include_file_time = cls.get_latest_include_file_time(
            project_configuration.path_resolver,
        )

        return ProjectTimestamps(
            files_timestamps,
            target_file_time,
            latest_include_file_time,
        )

    @classmethod
    def create_files_timestamps(
        cls,
        path_resolver: ProjectPathResolver,
        build_mode: BuildMode,
    ) -> dict[Path, FileTimestamps]:
        source_files = list(path_resolver.source_directory.rglob("*.cpp"))
        if build_mode == BuildMode.TEST:
            source_files.extend(path_resolver.test_directory.rglob("*.cpp"))

        return {
            source_file: cls.create_file_timestamps(
                path_resolver,
                build_mode,
                source_file,
            )
            for source_file in source_files
        }

    @staticmethod
    def create_file_timestamps(
        path_resolver: ProjectPathResolver,
        build_mode: BuildMode,
        source_file: Path,
    ) -> FileTimestamps:
        source_file_time = datetime.fromtimestamp(source_file.stat().st_mtime)
        object_file = path_resolver.get_object_file(source_file, build_mode)
        object_file_time = (
            datetime.fromtimestamp(object_file.stat().st_mtime)
            if object_file.exists()
            else None
        )

        return FileTimestamps(
            source_file_time,
            object_file_time,
        )

    @staticmethod
    def get_latest_include_file_time(
        path_resolver: ProjectPathResolver,
    ) -> datetime | None:
        include_tree = [
            path_resolver.include_directory,
            *path_resolver.include_directory.rglob("*"),
        ]

        return max(
            (
                datetime.fromtimestamp(header_file.stat().st_mtime)
                for header_file in include_tree
            ),
            default=None,
        )

    @staticmethod
    def get_target_file_time(
        project_configuration: ProjectConfiguration,
        build_mode: BuildMode,
    ) -> datetime | None:
        target_file = project_configuration.target(build_mode)
        return (
            datetime.fromtimestamp(target_file.stat().st_mtime)
            if target_file.exists()
            else None
        )
