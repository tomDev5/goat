from goat.command.compile.compile_command_builder import CompileCommandBuilder


class CompileCommandBuilderFactory:
    @staticmethod
    def create(program: str) -> CompileCommandBuilder:
        raise NotImplementedError()
