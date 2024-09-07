import click
from click_option_group import optgroup
from os.path import exists, pardir, join, dirname
from os import remove
import sys

from loguru import logger


@click.command("create-config-file", help="Generate a skip config YAML file.")
@optgroup.group("Skip Config Options", help="")
@optgroup.option("--output", "-o", "output_file", help="Path to the output file.")
def create_config_file(output_file: str):
    """
    Create a YAML file that can be used to generate a skip config.

    The YAML file should have the following structure:

    apps:
      nodejs-goof:
        skip_endpoints:
        - path: '/destroy/:id'
          method: GET
          description: Destroy an endpoint
    """

    # Read the contents of ../diff_utils/config.yml
    with open(join(dirname(__file__), pardir, "diff_utils", "config.yml"), "r") as f:
        example = f.read()

    # Write the YAML file
    if exists(output_file):
        if click.confirm(f"Output file {output_file} already exists. Are you sure you want to overwrite it?"):
            remove(output_file)
            with open(output_file, "w") as f:
                f.write(example)
            sys.exit(0)
    logger.info(f"Writing example config file to {output_file}")
    with open(output_file, "w") as f:
        f.write(example)
