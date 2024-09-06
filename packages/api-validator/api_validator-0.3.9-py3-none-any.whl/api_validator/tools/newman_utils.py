from os.path import exists
from os import remove
import invoke
from loguru import logger


def run_newman(postman_file: str, csv_output_file: str):
    """
    Run newman with the provided postman collection file and output the results to a CSV file.
    """
    if exists(csv_output_file):
        remove(csv_output_file)
    logger.info(f"Running newman with postman collection file: {postman_file}")
    try:
        invoke.run(f"newman run {postman_file} --timeout 300000 --delay-request 300 --timeout-request 5000 --suppress-exit-code  --reporters csv,cli --insecure --reporter-csv-export {csv_output_file}", hide=False)
    except invoke.exceptions.UnexpectedExit as exc:
        print(f"Error: {exc.result.stderr}")
    logger.info(f"Wrote the CSV output to: {csv_output_file}")
