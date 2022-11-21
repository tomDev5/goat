from goat.project.project_configuration import ProjectConfiguration
from goat.project.project_path_resolver import ProjectPathResolver
from goat.template.template import Template


class ProjectInitializer:
    TEMPLATE_MAIN_FILE_NAME = "main.cc"
    TEMPLATE_TEST_FILE_NAME = "test.cc"

    @classmethod
    def initialize(cls, path_resolver: ProjectPathResolver):
        assert (
            not path_resolver.root_path.exists()
        ), "Project root directory already exists"

        path_resolver.root_path.mkdir(parents=True)
        path_resolver.source_directory.mkdir(parents=True)
        path_resolver.include_directory.mkdir(parents=True)
        path_resolver.test_directory.mkdir(parents=True)

        template_configuration_path = path_resolver.configuration_file
        template_main_path = (
            path_resolver.source_directory / cls.TEMPLATE_MAIN_FILE_NAME
        )
        template_test_path = path_resolver.test_directory / cls.TEMPLATE_TEST_FILE_NAME

        template_configuration_path.write_text(Template.CONFIGURATION.read())
        template_main_path.write_text(Template.MAIN.read())
        template_test_path.write_text(Template.TEST.read())
