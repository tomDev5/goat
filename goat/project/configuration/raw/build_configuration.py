from pydantic import BaseModel
from goat.project.configuration.raw.build_configuration_variant import (
    BuildConfigurationVariant,
)


class BuildConfiguration(BaseModel):
    all: BuildConfigurationVariant
    release: BuildConfigurationVariant
    debug: BuildConfigurationVariant
    test: BuildConfigurationVariant
