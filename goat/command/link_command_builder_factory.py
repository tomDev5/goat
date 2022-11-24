from goat.command.link_command_builder import LinkCommandBuilder


class LinkCommandBuilderFactory:
    @staticmethod
    def create(program: str) -> LinkCommandBuilder:
        raise NotImplementedError()
