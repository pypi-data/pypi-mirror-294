import click
from api_validator.diff_utils.jobs import JobsContainer, read_jobs_from_yaml


@click.command("list-jobs", help="List all jobs in the config file.")
@click.option('--language', default=None, help='Filter jobs by programming language')
@click.option("--config-file", "-c", help="The config file to use.", required=True, type=click.Path(exists=True), default="config.yml")
def list_jobs(language, config_file):
    jobs_container = read_jobs_from_yaml(config_file)
    # sort them by language then name
    jobs_container = sorted(jobs_container, key=lambda x: (x.language, x.name))
    for job in jobs_container:
        if language is None or job.language.lower() == language.lower():
            print(f"Language: {job.language}, Job Name: {job.name}, Repo: {job.repo}")

