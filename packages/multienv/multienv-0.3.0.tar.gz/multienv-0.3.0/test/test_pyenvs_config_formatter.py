"""Test module for pyenv config formatters."""


from multienv._pyenvs_config_formatter import Formatters

def test_formatter_test():
    """Test formatter detection."""

    assert Formatters.CONDA.test('conda')
    assert not Formatters.CONDA.test('pip')
    assert Formatters.CONDA.test({'conda': {}})
