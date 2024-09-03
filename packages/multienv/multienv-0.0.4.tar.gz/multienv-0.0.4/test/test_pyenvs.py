"""Test module for pyenvs"""
from argparse import Namespace

from multienv.pyenvs import _create_parser

def test_info():
    """test info command"""

    parser = _create_parser()
    assert parser.parse_args(['info']) == Namespace(CMD='info')


def test_config_default():
    """test config command without supplying file"""

    parser = _create_parser()
    assert parser.parse_args(['config']) == Namespace(CMD='config', file='multienv.yml', encoding='utf-8')

def test_config_custom():
    """test config command supplying a custom file"""

    parser = _create_parser()
    assert parser.parse_args(['config', 'myenvs.yml']) == Namespace(CMD='config', file='myenvs.yml', encoding='utf-8')
