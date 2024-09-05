"""Pyenv config:
General standard input definition.
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class Dependency:
    """Representation of dependency features."""

    id: str
    version: str | None
    environments: list[str] | None
    source: str | None
    sha: str | None

    @staticmethod
    def from_dict(source: dict):
        """Builds a Dependency from a configuration dict."""

        assert 'id' in source, 'id is a mandatory dependency field'

        return Dependency(
            id=source['id'],
            version=str(source['version']) if 'version' in source else None,
            environments=source['environments'] if 'environments' in source else None,
            source=source['source'] if 'source' in source else None,
            sha=source['sha'] if 'sha' in source else None
        )

@dataclass(frozen=True)
class Configuration:
    """Representation of pyenvs configuration content."""

    formatters: list[dict, str]
    """Each formatter either can be a single character string of one of supported formatters or a key/value pair with 
    the key referencing to the formatter name and the value referencing to its specific configuration."""

    environments: list[str] | None
    """A reference list of the environments referenced by dependencies. If the list is provided, dependencies 
    referencing an unknown environment raise an error. If the list is not provided, it is inferred from the dependency
    environments. If an empty list is provided, no dependency is supposed to reference any specific environment."""

    dependencies: list[Dependency]
    """The list of the dependencies."""

    @staticmethod
    def from_dict(source: dict):
        """Builds a Configuration from a configuration dict."""
        return Configuration(
            formatters=source['configuration']['formatters'],
            environments=source['environments'] if 'environments' in source else None,
            dependencies=[Dependency.from_dict(d) for d in source['dependencies']]
        )
