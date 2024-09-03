"""
Pyenv config:
General Conda formatter output definitions.
"""

from dataclasses import dataclass

import yaml

from multienv._pyenvs_config_input_std import Dependency, Configuration

@dataclass(frozen=True)
class CondaEnvironment:
    """Conda environment file definition."""

    name: str
    channels: list[str]
    dependencies: list[str]

    def to_dict(self) -> dict:
        """Mapping to dict."""
        return {
            'name': self.name,
            'channels': self.channels,
            'dependencies': self.dependencies
        }

    def write(self, file_pattern: str, environment: str, encoding: str):
        """Write to yml output file."""
        with open(f'{file_pattern}{environment}.yml', "w", encoding=encoding) as o:
            yaml.dump(self.to_dict(), o, sort_keys=False)

    @staticmethod
    def from_configuration(name: str, channels: list[str], configuration: Configuration):
        """Build an environment from a standard configuration."""
        return CondaEnvironment.from_dependencies(name=name,
                                                  channels=channels,
                                                  dependencies=configuration.dependencies)

    @staticmethod
    def from_dependencies(name: str, channels: list[str], dependencies: list[Dependency]):
        """Build an environment from a dependency list."""
        return CondaEnvironment(name=name,
                                channels=channels,
                                dependencies=[CondaEnvironment._format_dependency(d) for d in dependencies])

    @staticmethod
    def _format_dependency(d: Dependency) -> str:
        """Formats a dependency to a conda dependency string."""
        result : str = d.id
        if d.version is not None:
            result += '=' + d.version
            if d.sha is not None:
                result += d.sha
        return result
