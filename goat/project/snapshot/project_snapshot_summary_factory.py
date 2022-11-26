from pathlib import Path
from goat.project.snapshot.project_snapshot import ProjectSnapshot
from goat.project.snapshot.project_snapshot_summary import ProjectSummary


class ProjectSummaryFactory:
    @classmethod
    def create(cls, project_snapshot: ProjectSnapshot) -> ProjectSummary:
        updated_files: list[tuple[Path, Path]] = []
        outdated_files: list[tuple[Path, Path]] = []
        for file_snapshot in project_snapshot.file_snapshots:
            outdated = False
            if file_snapshot.object_file_time is None:
                outdated = True
            elif file_snapshot.source_file_time > file_snapshot.object_file_time:
                outdated = True
            elif (
                project_snapshot.latest_include_file_time is not None
                and project_snapshot.latest_include_file_time
                > file_snapshot.object_file_time
            ):
                outdated = True

            source_file = file_snapshot.source_file
            object_file = file_snapshot.object_file

            if outdated:
                outdated_files.append((source_file, object_file))
            else:
                updated_files.append((source_file, object_file))

        target_file_outdated = False
        if project_snapshot.target_file_time is None:
            target_file_outdated = True
        elif len(outdated_files) > 0:
            target_file_outdated = True
        elif (
            project_snapshot.latest_object_file_time is not None
            and project_snapshot.latest_object_file_time
            > project_snapshot.target_file_time
        ):
            target_file_outdated = True

        return ProjectSummary(updated_files, outdated_files, target_file_outdated)
