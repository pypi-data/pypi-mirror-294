"""
Create a report detailing the validation results.
"""
from os.path import join, curdir
from os import listdir
from typing import List
from pathlib import Path
import yaml
import click
from api_validator.tools.newman_csv_data import NewmanData, NewmanReport, AppManager
from api_validator.tools.newman_csv_utils import combine_newman_csv


@click.command("report", help="Create a report detailing the validation results.")
@click.option("--data-dir", "-f", "data_directory", type=click.Path(exists=True), required=True, help="The analysis directory containing Newman CSV files")
@click.option("--config-file", "-c", help="The config file to use.", required=True, type=click.Path(exists=True), default="config.yml")
@click.option("--output-file", "-o", "output_file", default="newman_summary.md", help="Output file name")
def report(data_directory: str, config_file: str, output_file: str):
    run_report(data_directory, config_file, output_file)


def run_report(data_directory: str, config_file: str, output_file: str):
    combined_csv = join(curdir, "combined.csv")
    combine_newman_csv(output_file=combined_csv, artifact_directory=data_directory)
    newman_data = NewmanData(combined_csv)
    app_manager = AppManager(newman_data)
    # Create a list of app_names based on the CSVs in the data directory
    app_names = [Path(file).stem for file in listdir(data_directory) if
                 file.endswith('.csv') and "combined.csv" not in file]
    # app_details = {app_name: "" for app_name in app_names}
    app_details = get_app_details_from_config_file(config_file, app_names)
    newman_report = NewmanReport(app_manager, app_details=app_details)
    # Generate the markdown report
    newman_report.write_markdown_report(output_file)


def get_app_details_from_config_file(config_file: str, app_names: List[str]):
    """Get the app details from the config file."""
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    app_details = {}
    for app_name, app_details in config["apps"].items():
        if "repo" not in app_details or "language" not in app_details:
            app_details[app_name] = {"repo": "", "language": ""}
        else:
            app_details[app_name] = {"repo": app_details["repo"], "language": app_details["language"]}
    # Now add the ones that we gathered from the data directory
    for app_name in app_names:
        if app_name not in app_details:
            app_details[app_name] = {"repo": "", "language": ""}
    return app_details
