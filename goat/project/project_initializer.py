from goat.project.project_configuration import ProjectConfiguration
from goat.templates.template import Template


class ProjectInitializer:
    TEMPLATE_MAIN_FILE_NAME = "main.cc"
    TEMPLATE_TEST_FILE_NAME = "test.cc"

    @classmethod
    def initialize(cls, project_configuration: ProjectConfiguration):
        assert (
            not project_configuration.root_path.exists()
        ), "Project root directory already exists"

        project_configuration.root_path.mkdir()
        project_configuration.source_directory.mkdir()
        project_configuration.include_directory.mkdir()
        project_configuration.test_directory.mkdir()

        template_configuration_path = project_configuration.configuration_file
        template_main_path = (
            project_configuration.source_directory / cls.TEMPLATE_MAIN_FILE_NAME
        )
        template_test_path = (
            project_configuration.test_directory / cls.TEMPLATE_TEST_FILE_NAME
        )

        template_configuration_path.write_text(Template.CONFIGURATION.read())
        template_main_path.write_text(Template.MAIN.read())
        template_test_path.write_text(Template.TEST.read())
