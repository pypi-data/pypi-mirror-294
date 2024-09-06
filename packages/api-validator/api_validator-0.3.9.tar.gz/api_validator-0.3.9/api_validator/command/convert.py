import click
from click_option_group import optgroup

from api_validator.tools.openapi_to_postman import openapi_to_postman


@click.command("convert", help="Convert Swagger files to Postman collections.")
@optgroup.group("Swagger Options", help="")
@optgroup.option("--swagger-file", "-s", help="Path to the Swagger file.")
@optgroup.option("--postman-file", "-p", help="Path to the Postman file.")
@optgroup.option("--server", "-s", "server", required=True, help="The server for the API.")
def convert(swagger_file: str, postman_file: str, server: str):
    """
    Convert Swagger to Postman collection using openapi2postmanv2.
    """
    run_convert(swagger_file, postman_file, server)


def run_convert(swagger_file: str, postman_file: str, server: str):
    openapi_to_postman(swagger_file, postman_file, server)
