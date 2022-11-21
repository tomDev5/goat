from goat.project.project_path_resolver import ProjectPathResolver
from goat.template.template import Template


class ProjectInitializer:
    TEMPLATE_MAIN_FILE_NAME = "main.cc"
    TEMPLATE_TEST_FILE_NAME = "test.cc"

    @classmethod
    def initialize(cls, path_resolver: ProjectPathResolver):
        if path_resolver.root_path.exists():
            raise Exception("Project root directory already exists")

        path_resolver.root_path.mkdir(parents=True)
        path_resolver.source_directory.mkdir(parents=True)
        path_resolver.include_directory.mkdir(parents=True)
        path_resolver.test_directory.mkdir(parents=True)

        configuration_path = path_resolver.configuration_file
        main_path = path_resolver.source_directory / cls.TEMPLATE_MAIN_FILE_NAME
        test_path = path_resolver.test_directory / cls.TEMPLATE_TEST_FILE_NAME

        configuration_path.write_text(Template.CONFIGURATION.read())
        main_path.write_text(Template.MAIN.read())
        test_path.write_text(Template.TEST.read())
