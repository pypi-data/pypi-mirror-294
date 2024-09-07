from os.path import exists
from os import remove
import invoke
from loguru import logger


def run_newman(
        postman_file: str,
        csv_output_file: str,
        delay_request_ms: int = 300,
        timeout_request_ms: int = 5000
):
    """
    Run newman with the provided postman collection file and output the results to a CSV file.
    """
    if exists(csv_output_file):
        logger.info(f"Removing existing file: {csv_output_file}")
        remove(csv_output_file)
    logger.info(f"Running newman with postman collection file: {postman_file}")
    try:
        command = f"newman run {postman_file} --delay-request {delay_request_ms} --timeout-request {timeout_request_ms} --suppress-exit-code  --reporters csv,cli --insecure --reporter-csv-export {csv_output_file}"
        print(f"Running command: {command}")
        process = invoke.run(command, hide=False)
        if not exists(csv_output_file):
            logger.error(f"Failed to run newman with postman collection file: {postman_file}")
            print(f"Return code: {process.return_code}")
            print(f"stderr: {process.stderr}")
            print(f"stdout: {process.stdout}")
            raise Exception(f"Failed to run newman with postman collection file: {postman_file}")
    except invoke.exceptions.UnexpectedExit as exc:
        print(f"Error: {exc.result.stderr}")
    logger.info(f"Wrote the CSV output to: {csv_output_file}")
