from pydantic import BaseModel
from goat.configuration.build_configuration_values import (
    BuildConfigurationValues,
)


class BuildConfiguration(BaseModel):
    all: BuildConfigurationValues
    release: BuildConfigurationValues
    debug: BuildConfigurationValues
    test: BuildConfigurationValues
