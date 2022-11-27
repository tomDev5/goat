from pathlib import Path
from goat.command.command import Command
from goat.project.configuration.schema.packages_configuration_schema \
    import PackagesConfigurationSchema
from goat.project.project_path_resolver import ProjectPathResolver


class ConanCommandFactory():
    @staticmethod
    def format_requirement(requirement: str, version: str) -> str:
        return requirement + "/" + version

    @classmethod
    def save_conanfile(cls, formatted_requirements, conan_dir: Path):
        conan_dir.mkdir(exist_ok=True)
        with open(conan_dir.joinpath("conanfile.txt"), "w") as conanfile:
            conanfile.write("[requires]\n")
            for r in formatted_requirements:
                conanfile.write(r+"\n")

    @classmethod
    def build_conan_command(cls, packages: PackagesConfigurationSchema,
                            path_resolver: ProjectPathResolver) -> Command:  # Todo transfer parameters as parameter class???
        requirements = packages.requirements
        conan_dir = path_resolver.conan_directory

        formatted_requirements = [cls.format_requirement(key, requirements[key])
                                  for key in packages.requirements]
        cls.save_conanfile(formatted_requirements, conan_dir)

        executable = "conan"
        args = ["install", "-if", conan_dir, "-of", conan_dir, conan_dir]
        env = {"CONAN_USER_HOME": path_resolver.root_path}

        return Command(executable, args, env)
