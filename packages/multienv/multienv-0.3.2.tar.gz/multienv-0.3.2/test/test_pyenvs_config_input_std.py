"""Test module for pyenv config input."""

import pytest

from multienv._pyenvs_config_input_std import Dependency

def test_dependency_from_dict_classic():
    """Test dependency loading from dict."""

    i = {
        'id': 'multienv',
        'version': '0.0.2',
        'environments': ['multienv', 'test']
    }

    d = Dependency.from_dict(i)

    assert d.id == 'multienv'
    assert d.version == '0.0.2'
    assert d.environments == ['multienv', 'test']
    assert d.sha is None
    assert d.source is None


def test_dependency_from_dict_single_id():
    """Test dependency loading from dict."""

    i = {
        'id': 'multienv'
    }

    d = Dependency.from_dict(i)

    assert d.id == 'multienv'
    assert d.version is None
    assert d.environments is None
    assert d.sha is None
    assert d.source is None


def test_dependency_from_dict_without_id():
    """Test dependency loading from dict."""

    i = {
        'version': '0.0.2',
        'environments': ['multienv', 'test']
    }

    with pytest.raises(AssertionError) as e:
        Dependency.from_dict(i)

    assert e.value.args[0] == 'id is a mandatory dependency field'
