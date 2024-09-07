from os.path import join, dirname, exists, abspath, expanduser

import click
from click_option_group import optgroup, RequiredMutuallyExclusiveOptionGroup

from api_validator.diff_utils.jobs import JobsContainer, read_jobs_from_yaml
from api_validator.swagger_gen.api_extractor import api_extractor
from api_validator.tools.prerequisite_utils import validate_nightvision_installation
from api_validator.shared.click_validators import validate_internal_binary_path


@click.command("compare", help="Compare NV-generated Swagger vs. existing Swagger.")
@optgroup.group('Target Selection', cls=RequiredMutuallyExclusiveOptionGroup)
@optgroup.option('--language', default=None, help='Filter jobs by programming language')
@optgroup.option('--job', 'job_name', default=None, help='Specify a single job to run')
@optgroup.option('--all', 'run_all', is_flag=True, default=False, help='Run all jobs')
@optgroup.group('Output')
@optgroup.option('--output-file', '-o', help='Output file to write results to.')
@optgroup.group('Config File Options')
@optgroup.option("--config-file", "-c", help="The config file to use.", required=True, type=click.Path(exists=True), default="config.yml")
@optgroup.group('Internal Binary Options')
@optgroup.option("--internal", "internal", is_flag=True, default=False, help="Run internal API Extractor instead of NightVision CLI.")
@optgroup.option('--binary', 'binary_path', envvar='API_EXCAVATOR_BINARY', help='Path to API Extractor binary')
def compare(language: str, job_name: str, run_all: bool, output_file: str, config_file: str, internal: bool, binary_path: str):
    jobs_container = read_jobs_from_yaml(config_file)
    if internal:
        binary_path = validate_internal_binary_path(binary_path)

    filtered_jobs_container = JobsContainer()

    if run_all:
        filtered_jobs_container = jobs_container
    else:
        for job in jobs_container:
            if job_name and job.name == job_name:
                filtered_jobs_container.add_job(job)
                break
            elif language and job.language.lower() == language.lower():
                filtered_jobs_container.add_job(job)

    if len(filtered_jobs_container) == 0:
        print("No jobs found matching criteria.")
        return

    validate_nightvision_installation()
    report_name = "API Extraction Summary"
    if job_name:
        report_name = f"{job_name}: API Extraction Summary"
    elif language:
        report_name = f"{language}: API Extraction Summary"
    elif run_all:
        report_name = "All Jobs: API Extraction Summary"
    api_extractor(jobs_container=filtered_jobs_container, output_file=output_file, report_name=report_name, binary_path=binary_path, internal=internal)
