"""
Generate an OpenAPI spec by analyzing code using NightVision.
"""

import click
from click_option_group import optgroup


@click.command("generate", help="Generate Swagger docs from code using NightVision.")
@optgroup.group('Input')
@optgroup.option("--job", "-j", "job_name", help="Specify a single job to run.")
@optgroup.group('Output')
@optgroup.option('--output-file', '-o', help='Output file to write results to.')
@optgroup.group('Config')
@optgroup.option("--config-file", "-c", help="The config file to use.", required=True, type=click.Path(exists=True), default="config.yml")
@optgroup.group('Execution Options')
@optgroup.option('--binary', 'binary_path', envvar='API_EXCAVATOR_BINARY', default=None, help='Path to API Extractor binary')
def generate(job_name: str, output_file: str, config_file: str, binary_path: str):
    run_generate()


def run_generate():
    raise NotImplementedError("This command is not implemented yet.")
