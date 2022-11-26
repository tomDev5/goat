from goat.project.build_mode import BuildMode
from goat.project.configuration.project_configuration import ProjectConfiguration
from goat.project.snapshot.project_file_snapshot import ProjectFileSnapshot
from goat.project.snapshot.project_snapshot import ProjectSnapshot


class ProjectSnapshotFactory:
    @staticmethod
    def create(
        project_configuration: ProjectConfiguration,
        build_mode: BuildMode,
    ) -> ProjectSnapshot:
        path_resolver = project_configuration.path_resolver

        header_files = [path_resolver.include_directory]
        header_files += list(path_resolver.include_directory.rglob("*"))
        latest_include_file_modified = max(
            (header_file.stat().st_mtime for header_file in header_files)
        )

        source_files = list(path_resolver.source_directory.rglob("*.cpp"))
        if build_mode == BuildMode.TEST:
            source_files.extend(path_resolver.test_directory.rglob("*.cpp"))

        latest_object_file_modified: float | None = None
        outdated_file_snapshots: list[ProjectFileSnapshot] = []
        updated_file_snapshots: list[ProjectFileSnapshot] = []

        for source_file in source_files:
            source_file_time_modified = source_file.stat().st_mtime
            object_file = path_resolver.object_file(source_file, build_mode)
            object_file_time_modified = (
                object_file.stat().st_mtime if object_file.exists() else None
            )

            if latest_object_file_modified is None:
                latest_object_file_modified = object_file_time_modified
            elif object_file_time_modified is not None:
                latest_object_file_modified = max(
                    latest_object_file_modified,
                    object_file_time_modified,
                )

            project_file_snapshot = ProjectFileSnapshot(
                source_file,
                object_file,
            )

            outdated = False
            if object_file_time_modified is None:
                outdated = True
            elif source_file_time_modified > object_file_time_modified:
                outdated = True
            elif latest_include_file_modified > object_file_time_modified:
                outdated = True

            if outdated:
                outdated_file_snapshots.append(project_file_snapshot)
            else:
                updated_file_snapshots.append(project_file_snapshot)

        target_file_modified_time = (
            project_configuration.target(build_mode).stat().st_mtime
            if object_file.exists()
            else None
        )

        target_file_updated = True
        if len(outdated_file_snapshots) > 0:
            target_file_updated = False
        elif target_file_modified_time is None:
            target_file_updated = False
        elif (
            latest_object_file_modified is not None
            and latest_object_file_modified > target_file_modified_time
        ):
            target_file_updated = False

        return ProjectSnapshot(
            outdated_file_snapshots,
            updated_file_snapshots,
            target_file_updated,
        )
