from pathlib import Path
from goat.project.snapshot.project_snapshot import ProjectSnapshot
from goat.project.snapshot.project_snapshot_summary import ProjectSummary


class ProjectSummaryFactory:
    @classmethod
    def create(cls, project_snapshot: ProjectSnapshot) -> ProjectSummary:
        updated_files, outdated_files = cls.get_updated_outdated_files(project_snapshot)
        target_file_outdated = cls.is_target_file_outdated(
            project_snapshot,
            len(outdated_files) > 0,
        )

        return ProjectSummary(updated_files, outdated_files, target_file_outdated)

    @staticmethod
    def get_updated_outdated_files(
        project_snapshot: ProjectSnapshot,
    ) -> tuple[list[tuple[Path, Path]], list[tuple[Path, Path]]]:
        updated_files: list[tuple[Path, Path]] = []
        outdated_files: list[tuple[Path, Path]] = []
        for file_snapshot in project_snapshot.file_snapshots:
            source_file = file_snapshot.source_file
            object_file = file_snapshot.object_file

            outdated = ProjectSummaryFactory.is_file_snapshot_outdated(
                project_snapshot,
                file_snapshot,
            )

            if outdated:
                outdated_files.append((source_file, object_file))
            else:
                updated_files.append((source_file, object_file))

        return updated_files, outdated_files

    @staticmethod
    def is_file_snapshot_outdated(project_snapshot, file_snapshot):
        if file_snapshot.object_file_time is None:
            return True

        elif file_snapshot.source_file_time > file_snapshot.object_file_time:
            return True

        elif (
            project_snapshot.latest_include_file_time is not None
            and project_snapshot.latest_include_file_time
            > file_snapshot.object_file_time
        ):
            return True

        return False

    @staticmethod
    def is_target_file_outdated(
        project_snapshot: ProjectSnapshot,
        has_outdated_files: bool,
    ) -> bool:
        if project_snapshot.target_file_time is None:
            return True

        elif has_outdated_files:
            return True

        elif (
            project_snapshot.latest_object_file_time is not None
            and project_snapshot.latest_object_file_time
            > project_snapshot.target_file_time
        ):
            return True

        return False
