#! /usr/bin/env python3

import click
from api_validator.bin.logger import init_logger
from api_validator.command.convert import convert
from api_validator.command.create_config_file import create_config_file
from api_validator.command.exclude import exclude
from api_validator.command.generate import generate
from api_validator.command.install import install
from api_validator.command.list_jobs import list_jobs
from api_validator.command.report import report
from api_validator.command.validate import validate
from api_validator.command.yolo_traffic import yolo_traffic
from api_validator.command.compare import compare
from api_validator.version import __version__


@click.group
@click.version_option(version=__version__)
def api_validator():
    """Validate OpenAPI specs with traffic."""
    init_logger()


api_validator.add_command(compare)
api_validator.add_command(convert)
api_validator.add_command(create_config_file)
api_validator.add_command(exclude)
api_validator.add_command(generate)
api_validator.add_command(install)
api_validator.add_command(list_jobs)
api_validator.add_command(report)
api_validator.add_command(validate)
api_validator.add_command(yolo_traffic)


def main():
    """Validate OpenAPI specs with traffic."""
    api_validator()


if __name__ == '__main__':
    main()
