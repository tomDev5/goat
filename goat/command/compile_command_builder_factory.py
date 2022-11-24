from goat.command.compile_command_builder import CompileCommandBuilder


class CompileCommandBuilderFactory:
    @staticmethod
    def create(program: str) -> CompileCommandBuilder:
        raise NotImplementedError()
