from pathlib import Path
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

        source_files = list(path_resolver.source_directory.rglob("*.cpp"))
        if build_mode == BuildMode.TEST:
            source_files.extend(path_resolver.test_directory.rglob("*.cpp"))

        project_file_snapshots: list[ProjectFileSnapshot] = []
        for source_file in source_files:
            source_file_modified = source_file.stat().st_mtime
            object_file = path_resolver.object_file(source_file)
            object_file_modified = (
                object_file.stat().st_mtime if object_file.exists() else None
            )

            project_file_snapshot = ProjectFileSnapshot(
                source_file,
                source_file_modified,
                object_file,
                object_file_modified,
            )

            project_file_snapshots.append(project_file_snapshot)

        target_file_modified = (
            project_configuration.target(build_mode).stat().st_mtime
            if object_file.exists()
            else None
        )

        return ProjectSnapshot(project_file_snapshots, target_file_modified)
