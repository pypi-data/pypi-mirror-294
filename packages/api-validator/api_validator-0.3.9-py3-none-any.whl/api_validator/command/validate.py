"""
Send traffic to the endpoints specified in the Postman collection using Newman.
"""
import click
from os import makedirs
from api_validator.tools.newman_utils import run_newman


@click.command("validate", help="Validate Postman collections by sending traffic.")
@click.option("--postman-file", "-c", "postman_file", required=True, help="Postman collection file")
@click.option("--app-name", "-a", "app_name", required=True, help="App name for config and output file naming.")
@click.option("--output-dir", "-f", "output_directory", required=True, help="Output directory for the analysis data.")
def validate(postman_file: str, app_name: str, output_directory: str):
    run_validate(postman_file, app_name, output_directory)


def run_validate(postman_file: str, app_name: str, output_directory: str):
    makedirs(output_directory, exist_ok=True)
    output_file = f"{output_directory}/{app_name}.csv"
    run_newman(postman_file, output_file)
