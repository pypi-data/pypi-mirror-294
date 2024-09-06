"""Test module for pyenvs"""
from argparse import Namespace
from pathlib import Path

import pytest
import yaml

from multienv.pyenvs import _create_parser, _config

def _input_file(file: str) -> str:
    """Les fichiers d'entrée se trouvent à côté des scripts de test."""
    return str(Path(Path(__file__).parent, file))

def _output_file(file: str) -> str:
    """Les fichiers de sortie sont générés relativement à l'endroit où la commande est exécutée."""
    return str(Path(Path.cwd(), file))

def test_info_args():
    """test info command"""

    parser = _create_parser()
    assert parser.parse_args(['info']) == Namespace(CMD='info')


def test_config_args_default():
    """test config command without supplying file"""

    parser = _create_parser()
    assert parser.parse_args(['config']) == Namespace(CMD='config', file='multienv.yml', encoding='utf-8', output='.')

def test_config_args_custom():
    """test config command supplying a custom file"""

    parser = _create_parser()
    assert (parser.parse_args(['config', 'myenvs.yml'])
            == Namespace(CMD='config', file='myenvs.yml', encoding='utf-8', output='.'))

def test_config_without_default_env():
    """test config call without default env"""

    _config(Namespace(CMD='config', file=_input_file('multienv1.yml'), encoding='utf-8', output='.'))

    with open(_output_file('tutu_lint.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)
        assert content == {
            'name': 'lint',
            'channels': ['default', 'cosmoloj'],
            'dependencies': ['python=3.11', 'pylint=3.2.2']
        }

    with open(_output_file('tutu_test.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)
        assert content == {
            'name': 'test',
            'channels': ['default', 'cosmoloj'],
            'dependencies': ['python=3.11', 'pytest=7.4.4']
        }

    with pytest.raises(FileNotFoundError) as e:
        with open(_output_file('tutu_default.yml'), encoding='utf-8') as s:
            yaml.safe_load(s)

    assert e.value.args[0] == 2
    assert e.value.args[1] == "No such file or directory"


def test_config_without_channels():
    """test config call without channels"""

    _config(Namespace(CMD='config', file=_input_file('multienv2.yml'), encoding='utf-8', output='.'))

    with open(_output_file('tata_lint.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)
        assert content == {
            'name': 'lint',
            'dependencies': ['python=3.11', 'pylint=3.2.2']
        }

    with open(_output_file('tata_test.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)
        assert content == {
            'name': 'test',
            'dependencies': ['python=3.11', 'pytest=7.4.4']
        }

    with open(_output_file('tata_default.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)
        assert content == {
            'name': 'default',
            'dependencies': ['python=3.11', 'pylint=3.2.2', 'pytest=7.4.4']
        }


def test_config_without_environments():
    """test config call without environment list"""

    _config(Namespace(CMD='config', file=_input_file('multienv3.yml'), encoding='utf-8', output='.'))

    with open(_output_file('toto_lint.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)
        assert content == {
            'name': 'lint',
            'dependencies': ['python=3.11', 'pylint=3.2.2']
        }

    with open(_output_file('toto_test.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)
        assert content == {
            'name': 'test',
            'dependencies': ['python=3.11', 'pytest=7.4.4']
        }

    with open(_output_file('toto_default.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)
        assert content == {
            'name': 'default',
            'dependencies': ['python=3.11', 'pylint=3.2.2', 'pytest=7.4.4']
        }


def test_config_with_lacking_env_content():
    """test config call without an expected env in list"""

    with pytest.raises(ValueError) as e:
        _config(Namespace(CMD='config', file=_input_file('multienv2_lacking_env.yml'), encoding='utf-8', output='.'))

    assert e.value.args[0] == ("if defined, environment list ['lint'] should match "
                               "the implicit environment dependency set ['lint', 'test']")

    with pytest.raises(FileNotFoundError) as e:
        with open(_output_file('lacking_env_lint.yml'), encoding='utf-8') as s:
            yaml.safe_load(s)

    assert e.value.args[0] == 2
    assert e.value.args[1] == "No such file or directory"

    with pytest.raises(FileNotFoundError) as e:
        with open(_output_file('lacking_env_test.yml'), encoding='utf-8') as s:
            yaml.safe_load(s)

    assert e.value.args[0] == 2
    assert e.value.args[1] == "No such file or directory"

    with pytest.raises(FileNotFoundError) as e:
        with open(_output_file('lacking_env_default.yml'), encoding='utf-8') as s:
            yaml.safe_load(s)

    assert e.value.args[0] == 2
    assert e.value.args[1] == "No such file or directory"


def test_config_with_unexpected_env_content():
    """test config call with an unexpected env in list"""

    with pytest.raises(ValueError) as e:
        _config(Namespace(CMD='config', file=_input_file('multienv2_unexpected_env.yml'), encoding='utf-8', output='.'))

    assert e.value.args[0] == ("if defined, environment list ['lint', 'test', 'unexpected'] should match "
                               "the implicit environment dependency set ['lint', 'test']")

    with pytest.raises(FileNotFoundError) as e:
        with open(_output_file('unexpected_env_lint.yml'), encoding='utf-8') as s:
            yaml.safe_load(s)

    assert e.value.args[0] == 2
    assert e.value.args[1] == "No such file or directory"

    with pytest.raises(FileNotFoundError) as e:
        with open(_output_file('unexpected_env_test.yml'), encoding='utf-8') as s:
            yaml.safe_load(s)

    assert e.value.args[0] == 2
    assert e.value.args[1] == "No such file or directory"

    with pytest.raises(FileNotFoundError) as e:
        with open(_output_file('unexpected_lacking_env_default.yml'), encoding='utf-8') as s:
            yaml.safe_load(s)

    assert e.value.args[0] == 2
    assert e.value.args[1] == "No such file or directory"


def test_config_with_pip_dependencies():
    """test config call with pip dependencies"""

    _config(Namespace(CMD='config', file=_input_file('multienv_pip.yml'), encoding='utf-8', output='.'))

    with open(_output_file('pip_lint.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)
        assert content == {
            'name': 'lint',
            'channels': ['default', 'cosmoloj'],
            'dependencies': [
                'python=3.12',
                {
                    'pip': ['pyyaml==6.0.1', 'pylint==3.2.2']
                }]
        }

    with open(_output_file('pip_test.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)
        assert content == {
            'name': 'test',
            'channels': ['default', 'cosmoloj'],
            'dependencies': [
                'python=3.12',
                'pytest=7.4.4',
                'multienv=0.0.2',
                {
                    'pip': ['pyyaml==6.0.1']
                }]
        }


    with open(_output_file('pip_multienv.yml'), encoding='utf-8') as s:
        content = yaml.safe_load(s)
        print(content)
        assert content == {
            'name': 'multienv',
            'channels': ['default', 'cosmoloj'],
            'dependencies': [
                'python=3.12',
                'multienv=0.0.2',
                {
                    'pip': ['pyyaml==6.0.1']
                }]
        }

    with pytest.raises(FileNotFoundError) as e:
        with open(_output_file('pip_default.yml'), encoding='utf-8') as s:
            yaml.safe_load(s)

    assert e.value.args[0] == 2
    assert e.value.args[1] == "No such file or directory"
