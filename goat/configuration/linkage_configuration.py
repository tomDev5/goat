from goat.configuration.linkage_configuration_values import (
    LinkageConfigurationValues,
)


class LinkageConfiguration(LinkageConfigurationValues):
    release: LinkageConfigurationValues
    debug: LinkageConfigurationValues
    test: LinkageConfigurationValues
