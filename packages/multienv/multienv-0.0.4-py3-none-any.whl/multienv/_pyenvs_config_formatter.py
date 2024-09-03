"""Pyenvs config:
Formatter definitions.

Supported formatters:
- conda
"""

from dataclasses import dataclass
from enum import Enum
from typing import Callable

from multienv._pyenvs_config_input_std import Configuration
from multienv._pyenvs_config_output_conda import CondaEnvironment

@dataclass(frozen=True)
class CondaConfiguration:
    """The specific conda configuration model."""

    default_environment: bool
    file_pattern: str
    encoding: str
    channels: list[str]

    @staticmethod
    def from_configuration(formatter: dict | str):
        """Builds a conda configuration object form a dict or a default one form a string"""

        if isinstance(formatter, str):
            return _DEFAULT_CONDA_CONFIGURATION

        body = formatter[Formatters.CONDA.value.name]

        return CondaConfiguration(
            default_environment=body['default_environment'] if 'default_environment' in body
            else _DEFAULT_CONDA_CONFIGURATION.default_environment,
            file_pattern=body['file_pattern'] if 'file_pattern' in body else _DEFAULT_CONDA_CONFIGURATION.file_pattern,
            encoding=body['encoding'] if 'encoding' in body else _DEFAULT_CONDA_CONFIGURATION.encoding,
            channels=body['channels'] if 'channels' in body else _DEFAULT_CONDA_CONFIGURATION.channels
        )

_DEFAULT_CONDA_CONFIGURATION = CondaConfiguration(
    default_environment=True,
    file_pattern='environment',
    encoding='utf-8',
    channels=['default']
)

def conda_writer(configuration: Configuration):
    """Writes a configuration as conda configuration environment files."""

    formatter_configuration: CondaConfiguration = Formatters.CONDA.get_formatter_configuration(configuration)

    # default environment includes all dependencies
    if formatter_configuration.default_environment:

        env = CondaEnvironment.from_configuration(name='default',
                                                  channels=formatter_configuration.channels,
                                                  configuration=configuration)
        env.write(file_pattern=formatter_configuration.file_pattern,
                  environment="_",
                  encoding=formatter_configuration.encoding)

    if configuration.environments is None:
        return

    for e in configuration.environments:

        env = CondaEnvironment.from_dependencies(name=e,
                                                 channels=formatter_configuration.channels,
                                                 dependencies=[d for d in configuration.dependencies
                                                               if d.environments is None or e in d.environments])
        env.write(file_pattern=formatter_configuration.file_pattern,
                  environment=f"_{e}",
                  encoding=formatter_configuration.encoding)

@dataclass(frozen=True)
class _FormatterValue[C]:
    name: str
    write: Callable[[Configuration], None]
    configuration: Callable[[dict | str], C]


class Formatters(Enum):
    """The enumeration of the supported formatters."""
    CONDA = _FormatterValue[CondaConfiguration](name='conda',
                                                write=conda_writer,
                                                configuration=CondaConfiguration.from_configuration)

    def test(self, formatter: dict | str) -> bool:
        """Checks if a formatter configuration dict refers to the current Formatter value."""
        return (isinstance(formatter, str) and self.value.name == formatter
                or isinstance(formatter, dict) and self.value.name in formatter)

    def get_formatter_configuration(self, configuration: Configuration):
        """Builds a specific formatter configuration from the main configuration related to the current Formatter value.
        """
        for formatter in configuration.formatters:
            if self.test(formatter):
                return self.value.configuration(formatter)
        raise ValueError
