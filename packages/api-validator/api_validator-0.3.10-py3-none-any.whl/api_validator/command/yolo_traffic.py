import click
from os.path import curdir, join
from os import makedirs
from click_option_group import optgroup
from api_validator.command.install import run_install
from api_validator.command.convert import run_convert
from api_validator.command.exclude import run_exclude_postman_request
from api_validator.command.validate import run_validate
from api_validator.command.report import run_single_report
from api_validator.command.generate import run_generate


@click.command("yolo-traffic", help="Run the entire workflow in one command.")
@optgroup.group("Required files", help="")
@optgroup.option("--config-file", "-c", help="The config file to use.", required=True, type=click.Path(exists=True), default="config.yml")
@optgroup.option("--swagger-file", "-s", help="The OpenAPI file to validate.", required=True, type=click.Path(exists=True))
@optgroup.option("--postman-file", "-p", help="The Postman file to create.", default="postman.json", type=click.Path(exists=False))
@optgroup.option("--report-file", "-r", help="The report file to create.", default="summary.md", type=click.Path(exists=False))
@optgroup.group("Other arguments")
@optgroup.option("--app-name", "-a", "app_name", help="App name in the config.", required=True)
@optgroup.option("--server", "-s", "server", help="The server for the API.", required=True)
@optgroup.group("Optional Newman arguments")
@optgroup.option("--delay-request", "-d", default=300, type=int, help="Delay between requests in milliseconds.")
@optgroup.option("--timeout-request", "-r", default=5000, type=int, help="Request timeout in milliseconds.")
def yolo_traffic(
    swagger_file: str,
    postman_file: str,
    config_file: str,
    report_file: str,
    app_name: str,
    server: str,
    delay_request: int,
    timeout_request: int
):
    output_directory = join(curdir, "newman-data")
    makedirs(output_directory, exist_ok=True)
    run_install(check_only=False, force=False)
    # run_generate()
    run_convert(
        server=server,
        swagger_file=swagger_file,
        postman_file=postman_file
    )
    run_exclude_postman_request(
        postman_file=postman_file,
        app_name=app_name,
        config_file=config_file
    )
    # Run newman and output
    csv_file = run_validate(
        postman_file=postman_file,
        output_directory=output_directory,
        app_name=app_name,
        delay_request_ms=delay_request,
        timeout_request_ms=timeout_request
    )
    run_single_report(
        data_directory=output_directory,
        config_file=config_file,
        output_file=report_file,
        combined_csv_file=csv_file,
        app_name=app_name
    )
