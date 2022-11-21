from goat.configuration.compilation_configuration_values import (
    CompilationConfigurationValues,
)


class CompilationConfiguration(CompilationConfigurationValues):
    release: CompilationConfigurationValues
    debug: CompilationConfigurationValues
    test: CompilationConfigurationValues
