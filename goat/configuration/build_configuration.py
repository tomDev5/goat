from pydantic import BaseModel
from goat.configuration.build_configuration_entry import (
    BuildConfigurationEntry,
)


class BuildConfiguration(BaseModel):
    all: BuildConfigurationEntry
    release: BuildConfigurationEntry
    debug: BuildConfigurationEntry
    test: BuildConfigurationEntry
