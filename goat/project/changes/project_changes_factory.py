from pathlib import Path
from goat.project.changes.file_timestamps import FileTimestamps
from goat.project.changes.project_timestamps import ProjectTimestamps
from goat.project.changes.project_changes import ProjectChanges


class ProjectChangesFactory:
    @classmethod
    def create(cls, project_timestamps: ProjectTimestamps) -> ProjectChanges:
        changed_files, unchanged_files = cls.get_changed_unchanged_files(
            project_timestamps
        )

        target_file_changed = cls.is_target_file_changed(
            project_timestamps,
            len(changed_files) > 0,
        )

        return ProjectChanges(changed_files, unchanged_files, target_file_changed)

    @staticmethod
    def get_changed_unchanged_files(
        project_timestamps: ProjectTimestamps,
    ) -> tuple[list[Path], list[Path]]:
        changed_files: list[Path] = []
        unchanged_files: list[Path] = []

        for source_file, file_timestamps in project_timestamps.files_timestamps.items():
            changed = ProjectChangesFactory.is_source_file_changed(
                project_timestamps,
                file_timestamps,
            )

            if changed:
                changed_files.append(source_file)
            else:
                unchanged_files.append(source_file)

        return changed_files, unchanged_files

    @staticmethod
    def is_source_file_changed(
        project_timestamps: ProjectTimestamps,
        file_timestamps: FileTimestamps,
    ):
        if file_timestamps.object_file_time is None:
            return True

        elif file_timestamps.source_file_time > file_timestamps.object_file_time:
            return True

        elif (
            project_timestamps.latest_include_file_time is not None
            and project_timestamps.latest_include_file_time
            > file_timestamps.object_file_time
        ):
            return True

        return False

    @staticmethod
    def is_target_file_changed(
        project_timestamps: ProjectTimestamps,
        has_changed_files: bool,
    ) -> bool:
        if project_timestamps.target_file_time is None:
            return True

        elif has_changed_files:
            return True

        elif (
            project_timestamps.latest_object_file_time is not None
            and project_timestamps.latest_object_file_time
            > project_timestamps.target_file_time
        ):
            return True

        return False
