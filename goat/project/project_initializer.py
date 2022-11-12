from goat.project.project_configuration import ProjectConfiguration
from goat.templates.template import Template


class ProjectInitializer:
    TEMPLATE_MAIN_FILE_NAME = "main.cc"
    TEMPLATE_TEST_FILE_NAME = "test.cc"

    @classmethod
    def initialize(cls, configuration: ProjectConfiguration):
        assert (
            not configuration.root_path.exists()
        ), "Project root directory already exists"

        configuration.root_path.mkdir()
        configuration.source_directory.mkdir()
        configuration.include_directory.mkdir()
        configuration.test_directory.mkdir()

        template_configuration_path = configuration.configuration_file
        template_main_path = (
            configuration.source_directory / cls.TEMPLATE_MAIN_FILE_NAME
        )
        template_test_path = configuration.test_directory / cls.TEMPLATE_TEST_FILE_NAME

        template_configuration_path.write_text(Template.CONFIGURATION.read())
        template_main_path.write_text(Template.MAIN.read())
        template_test_path.write_text(Template.TEST.read())
