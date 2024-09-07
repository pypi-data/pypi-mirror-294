"""
Send traffic to the endpoints specified in the Postman collection using Newman.
"""
import click
from click_option_group import optgroup
from os import makedirs
from api_validator.tools.newman_utils import run_newman


@click.command("validate", help="Validate Postman collections by sending traffic.")
@optgroup.group("Required files", help="")
@optgroup.option("--postman-file", "-c", "postman_file", required=True, help="Postman collection file")
@optgroup.option("--app-name", "-a", "app_name", required=True, help="App name for config and output file naming.")
@optgroup.option("--output-dir", "-f", "output_directory", required=True, help="Output directory for the analysis data.")
@optgroup.group("Optional Newman arguments")
@optgroup.option("--delay-request", "-d", default=300, type=int, help="Delay between requests in milliseconds.")
@optgroup.option("--timeout-request", "-r", default=5000, type=int, help="Request timeout in milliseconds.")
def validate(
        postman_file: str,
        app_name: str,
        output_directory: str,
        delay_request: int,
        timeout_request: int
):
    run_validate(postman_file, app_name, output_directory, delay_request, timeout_request)


def run_validate(
        postman_file: str,
        app_name: str,
        output_directory: str,
        delay_request_ms: int = 300,
        timeout_request_ms: int = 5000
) -> str:
    makedirs(output_directory, exist_ok=True)
    csv_file = f"{output_directory}/{app_name}.csv"
    run_newman(
        postman_file=postman_file,
        csv_output_file=csv_file,
        delay_request_ms=delay_request_ms,
        timeout_request_ms=timeout_request_ms
    )
    return csv_file
