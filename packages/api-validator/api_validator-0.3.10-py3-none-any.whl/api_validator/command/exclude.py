import click
from loguru import logger
from api_validator.tools.postman_utils import add_postman_exclusion


@click.group()
def exclude():
    """Commands to skip requests in a Postman collection."""
    pass


@exclude.command("postman-request", help="Modify a Postman collection to skip certain requests.")
@click.option("--postman-file", "-f", "postman_file", required=True, help="Output Postman file name")
@click.option("--app-name", "-a", "app_name", required=True, help="App name")
@click.option("--config-file", "-c", help="The config file to use.", required=True, type=click.Path(exists=True), default="config.yml")
def postman_request(postman_file: str, app_name: str, config_file: str):
    """
    Read a skip config file and skip the specified endpoints in the Postman collection.
    """
    logger.info(f"Adding Postman exclusion to {postman_file}")
    run_exclude_postman_request(postman_file, app_name, config_file)


def run_exclude_postman_request(postman_file: str, app_name: str, config_file: str):
    add_postman_exclusion(
        output_file=postman_file,
        collection_file=postman_file,
        app=app_name,
        config_file=config_file
    )
