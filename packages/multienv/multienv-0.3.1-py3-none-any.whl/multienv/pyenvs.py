"""
pyenvs command entrypoint
"""
import logging

from argparse import ArgumentParser, Namespace
from pathlib import Path

import yaml

from multienv._pyenvs_config_formatter import Configuration, Formatters

LOG = logging.getLogger(__name__)


def _info(ns: Namespace):
    """info
    """
    LOG.info("info")


def _config(ns: Namespace):
    """config
    """
    LOG.info("config")

    extension = ns.file.split('.')[-1]
    output_dir = Path(Path.cwd(), ns.output)

    if extension in ['yml']:
        LOG.info('open configuration file %s', ns.file)
        with open(ns.file, encoding=ns.encoding) as s:
            content = yaml.safe_load(s)
            configuration = Configuration.from_dict(content)

            LOG.debug('open configuration file content: %s', configuration)
            for req_formatter in configuration.formatters:
                for supported_formatter in Formatters:
                    if supported_formatter.test(req_formatter):
                        supported_formatter.value.write(configuration, output_dir)


    else:
        raise ValueError(f'unsupported configuration format {extension}')


def _create_parser() -> ArgumentParser:

    # parse argument line
    parser = ArgumentParser(description='Multi environment management.')

    subparsers = parser.add_subparsers(dest='CMD', help='available commands')

    subparsers.add_parser('info', help='get general info')

    parser_config = subparsers.add_parser('config', help='generates environment configurations')
    parser_config.add_argument('file',
                               nargs='?',
                               help="path to the configuration file",
                               default="multienv.yml")
    parser_config.add_argument('--encoding',
                               nargs='?',
                               help='the configuration file encoding (default to utf-8)',
                               default='utf-8')
    parser_config.add_argument('--output',
                               nargs='?',
                               help='the environment file output directory',
                               default='.')

    return parser


def entrypoint():
    """The pyenvs command entrypoint."""

    commands = {
        'info': _info,
        'config': _config
    }

    ns: Namespace = _create_parser().parse_args()

    commands[ns.CMD](ns)
