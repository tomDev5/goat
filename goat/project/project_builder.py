from goat.project.project_configuration import ProjectConfiguration


class ProjectBuilder:
    project_configuration: ProjectConfiguration

    def __init__(self, project_configuration: ProjectConfiguration) -> None:
        self.project_configuration = project_configuration
