"""Test module for pyenv conda environment output."""

from multienv._pyenvs_config_output_conda import CondaEnvironment
from multienv._pyenvs_config_input_std import Dependency

def test_to_dict():
    """Test dict representation of conda environment output."""

    env = CondaEnvironment(name="environment_name",
                           channels=["channel1", "channel2"],
                           pip_dependencies=["pip1", "pip2"],
                           dependencies=["pip1", "conda1", "pip2", "conda2"])

    assert env.to_dict() == {
        'name': 'environment_name',
        'channels': ['channel1', 'channel2'],
        'dependencies': ['pip1',
                         'conda1',
                         'pip2',
                         'conda2',
                         {
                             'pip': ['pip1', 'pip2']
                         }]
    }

def test_format_dependency():
    """Test dependency formatting for conda."""

    d = Dependency(id="d_id", version="d_version", environments=["env_a", "env_b"], source="d_source", sha="d_sha")

    assert CondaEnvironment._format_dependency(d=d) == "d_id=d_version=d_sha"
