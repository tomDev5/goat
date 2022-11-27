from goat.project.build_mode import BuildMode
from goat.project.configuration.project_configuration import ProjectConfiguration
from goat.project.project_path_resolver import ProjectPathResolver
from goat.project.snapshot.project_snapshot_entry import ProjectSnapshotEntry
from goat.project.snapshot.project_snapshot import ProjectSnapshot


class ProjectSnapshotFactory:
    @classmethod
    def create(
        cls,
        project_configuration: ProjectConfiguration,
        build_mode: BuildMode,
    ) -> ProjectSnapshot:
        file_snapshots = cls.get_file_snapshots(
            project_configuration.path_resolver,
            build_mode,
        )

        target_file_time = cls.get_target_file_time(project_configuration, build_mode)

        latest_object_file_time = max(
            (
                file_snapshot.object_file_time
                for file_snapshot in file_snapshots
                if file_snapshot.object_file_time is not None
            ),
            default=None,
        )

        latest_include_file_time = cls.get_latest_include_file_time(
            project_configuration.path_resolver,
        )

        return ProjectSnapshot(
            file_snapshots,
            target_file_time,
            latest_object_file_time,
            latest_include_file_time,
        )

    @staticmethod
    def get_file_snapshots(
        path_resolver: ProjectPathResolver,
        build_mode: BuildMode,
    ) -> list[ProjectSnapshotEntry]:
        source_files = list(path_resolver.source_directory.rglob("*.cpp"))
        if build_mode == BuildMode.TEST:
            source_files.extend(path_resolver.test_directory.rglob("*.cpp"))

        file_snapshots: list[ProjectSnapshotEntry] = []
        for source_file in source_files:
            source_file_time = source_file.stat().st_mtime
            object_file = path_resolver.get_object_file(source_file, build_mode)
            object_file_time = (
                object_file.stat().st_mtime if object_file.exists() else None
            )

            file_snapshot = ProjectSnapshotEntry(
                source_file,
                source_file_time,
                object_file,
                object_file_time,
            )

            file_snapshots.append(file_snapshot)

        return file_snapshots

    @staticmethod
    def get_latest_include_file_time(
        path_resolver: ProjectPathResolver,
    ) -> float | None:
        include_files = [path_resolver.include_directory]
        include_files += list(path_resolver.include_directory.rglob("*"))
        return max(
            (header_file.stat().st_mtime for header_file in include_files), default=None
        )

    @staticmethod
    def get_target_file_time(
        project_configuration: ProjectConfiguration,
        build_mode: BuildMode,
    ) -> float | None:
        target_file = project_configuration.target(build_mode)
        return target_file.stat().st_mtime if target_file.exists() else None
