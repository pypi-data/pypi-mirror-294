import os.path
import time
import requests
from os.path import join, pardir, dirname, exists, abspath
from os import makedirs, remove, curdir
from typing import Union
import shutil
import subprocess
import yaml
import invoke
import shlex

from api_validator.tools.oasdiff import OasdiffOutput


def remove_local_refs(data):
    """Workaround for: https://github.com/Tufin/oasdiff/issues/438"""
    allowed_refs = (
        "http://", "https://",
        # TODO: # Was getting a weird error from oasdiff so I had to comment out local refs to unmentioned schemas
        # Like when it would look like this:
        # "$ref": "#/components/schemas/ID"
        # So that is why the "#" is commented out.
        # "#"
    )
    if isinstance(data, dict):
        keys_to_delete = []
        for key, value in data.items():
            if key == "$ref" and isinstance(value, str) and not value.startswith(allowed_refs):
                return None  # Return None to indicate this item should be removed
            result = remove_local_refs(value)
            if result is None:
                keys_to_delete.append(key)
            else:
                data[key] = result
        for key in keys_to_delete:
            del data[key]
        return data
    elif isinstance(data, list):
        return [remove_local_refs(item) for item in data if remove_local_refs(item) is not None]
    else:
        return data


def remove_local_refs_from_file(file_path: str):
    with open(file_path, 'r') as base_file:
        base_data = yaml.safe_load(base_file)
    base_data = remove_local_refs(base_data)
    with open(file_path, 'w') as base_file:
        yaml.dump(base_data, base_file)


class Job:
    def __init__(self, name: str, repo: str, swagger_file: str, language: str, github_stars: int, subdirectory: str = None, include_path_params: bool = False, exclude_paths: list = None, use_config: str = None):
        self.name = name
        self.repo = repo
        self.swagger_file = swagger_file
        self.language = language
        self.github_stars = github_stars
        self.subdirectory = subdirectory
        self.include_path_params = include_path_params
        self.use_config = use_config
        self.exclude_paths = exclude_paths
        self.owner, self.repo_name = self._parse_repo(repo)
        # self.extension = splitext(swagger_file)[1][1:]  # Extract extension without the dot
        # It will always be saved as yaml. If we see a swagger file that is json, let's just load it to yaml for uniformity
        self.extension = "yml"
        self.local_base_swagger_file = abspath(join(curdir, 'analysis', 'base', f'{name}.{self.extension}'))
        self.local_revision_swagger_file = abspath(join(curdir, 'analysis', 'revision', f'{name}.yml'))
        self.local_repo = abspath(join(curdir, 'analysis', 'repos', self.repo_name))
        self.local_oasdiff_file = abspath(join(curdir, 'analysis', 'oasdiff', f"{name}.yml"))

    def __repr__(self):
        return f"Job(name={self.name!r}, repo={self.repo!r}, language={self.language!r}, github_stars={self.github_stars!r}, subdirectory={self.subdirectory!r})"

    def _parse_repo(self, repo_url):
        # Remove trailing /
        if repo_url.endswith('/'):
            repo_url = repo_url[:-1]
        parts = repo_url.split('/')
        return parts[-2], parts[-1]

    def clone(self):
        makedirs(dirname(self.local_repo), exist_ok=True)
        # if "github" in self.repo:
        #     command = f"gh repo clone {self.owner}/{self.repo_name} {self.local_repo} -- --depth 1"
        # else:
        command = f"git clone {self.repo} {self.local_repo} --depth 1"
        args = shlex.split(command)
        # command = f"git clone {self.repo} {self.local_repo}"
        # subprocess.run(['git', 'clone', self.repo, self.local_repo], check=True)
        process = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def clean(self):
        if exists(self.local_repo):
            # shutil remove the self.local_repo directory
            shutil.rmtree(self.local_repo)

    def download_base_swagger(self):
        makedirs(dirname(self.local_base_swagger_file), exist_ok=True)
        if exists(self.local_base_swagger_file):
            remove(self.local_base_swagger_file)
        # urlretrieve(self.swagger_file, self.local_base_swagger_file)
        url = self.swagger_file
        output_file = self.local_base_swagger_file
        try:
            # Send a GET request to the URL to download the file content
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Determine the file type based on the URL (JSON or YAML)
                if url.endswith('.json'):
                    # Load the JSON data
                    data = response.json()
                elif url.endswith('.yaml') or url.endswith('.yml'):
                    # Load the YAML data
                    data = yaml.safe_load(response.text)
                else:
                    # Try to load it as yaml first
                    try:
                        data = yaml.safe_load(response.text)
                    except yaml.YAMLError:
                        # If it fails, try to load it as JSON
                        data = response.json()
                    except:
                        raise ValueError("Unsupported file format. Supported formats: .json, .yaml, .yml")

                if os.path.exists(output_file):
                    os.remove(output_file)
                # Save the loaded data as a YAML file
                with open(output_file, 'w') as yaml_file:
                    yaml.dump(data, yaml_file, default_flow_style=False)

                print(f"\t{self.owner}/{self.repo_name}: Data downloaded from {url} and saved as {output_file}")
            else:
                print(f"\t{self.owner}/{self.repo_name}: Failed to download data from {url}. Status code: {response.status_code}")

        except Exception as e:
            print(f"\t{self.owner}/{self.repo_name}: An error occurred: {e}")

    def api_excavator_command(self, binary_path: str):
        if binary_path is None:
            binary_path = "api-excavator"
        else:
            if not exists(binary_path):
                raise Exception(f"Binary path does not exist: {binary_path}")
            # If it's a directory, then we need to join it with the binary name
            if os.path.isdir(binary_path):
                binary_path = join(binary_path, "api-excavator")
            # Otherwise, it's a file and we can just use that
        if self.subdirectory:
            local_repo_dir = os.path.join(self.local_repo, self.subdirectory)
            if not exists(local_repo_dir):
                raise ValueError(f"The subdirectory {self.subdirectory} is not valid. Check the path {local_repo_dir} to make sure.")
        else:
            local_repo_dir = self.local_repo
        command = f"{binary_path} --log-level info --output {self.local_revision_swagger_file} -l {self.language}"
        if self.use_config:
            command += f" --config \"configurations/{self.name}.nvexcavator\""
        command += f" {local_repo_dir}"
        return command

    def nightvision_command(self):
        if self.subdirectory:
            local_repo_dir = os.path.join(self.local_repo, self.subdirectory)
            if not exists(local_repo_dir):
                raise ValueError(f"The subdirectory {self.subdirectory} is not valid. Check the path {local_repo_dir} to make sure.")
        else:
            local_repo_dir = self.local_repo
        command = f"nightvision swagger extract {local_repo_dir} --output {self.local_revision_swagger_file} --lang {self.language} --no-upload"
        if self.use_config:
            command += f" --config \"configurations/{self.use_config}.nvexcavator\""
        return command

    def run_extraction(self, binary_path: str = None, internal: bool = False):
        if internal:
            command = self.api_excavator_command(binary_path)
        else:
            command = self.nightvision_command()

        print(f"\t\t{self.owner}/{self.repo_name}: Running command: {command}")
        # args = shlex.split(command)
        # process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        response = invoke.run(command, hide=True)
        stderr = response.stderr
        stdout = response.stdout
        # After running this, print the stderr and stdout
        # stderr = process.stderr.decode('utf-8')
        # For every line in stderr, put two tabs
        for line in stderr.splitlines():
            print(f"\t\t{self.owner}/{self.repo_name}: {line}")
        # stdout = process.stdout.decode('utf-8')
        for line in stdout.splitlines():
            print(f"\t\t{self.owner}/{self.repo_name}: {line}")

        if "0 paths discovered" in stderr:
            print(f"\t\t{self.owner}/{self.repo_name}: No paths discovered.")
            # If local_revision_swagger_file does not exist, that is because there were no paths discovered. Let's create an empty YAML file so that oasdiff has something to read
            if not exists(self.local_revision_swagger_file):
                makedirs(dirname(self.local_revision_swagger_file), exist_ok=True)
                with open(self.local_revision_swagger_file, 'w') as empty_yaml_file:
                    empty_yaml_file.write('openapi: 3.0.0\npaths: {}\n')

    def oasdiff(self, elapsed_time: float) -> Union[OasdiffOutput, None]:
        """Runs oasdiff and returns the OasdiffOutput object"""
        makedirs(dirname(self.local_oasdiff_file), exist_ok=True)
        if exists(self.local_oasdiff_file):
            remove(self.local_oasdiff_file)
        # Added --include-path-params, reason: https://github.com/Tufin/oasdiff/blob/d7c8034df3e2a65cda1f68cc5b3fc242b075ba47/MATCHING-ENDPOINTS.md?plain=1#L20
        command = f"oasdiff diff {self.local_base_swagger_file} {self.local_revision_swagger_file} --exclude-elements description,examples,title,summary"
        if self.include_path_params:
            command += " --include-path-params"
        args = shlex.split(command)
        # If local_revision_swagger_file does not exist, that is because there were no paths discovered. Let's create an empty YAML file so that oasdiff has something to read
        if not exists(self.local_revision_swagger_file):
            makedirs(dirname(self.local_revision_swagger_file), exist_ok=True)
            with open(self.local_revision_swagger_file, 'w') as empty_yaml_file:
                empty_yaml_file.write('openapi: 3.0.0\npaths: {}\n')
        process = None
        # First, before running oasdiff, we need to remove any local file references from the base file. It won't be in the revision file because NightVision doesn't do that.
        # This will help us avoid: https://github.com/Tufin/oasdiff/issues/438
        remove_local_refs_from_file(self.local_base_swagger_file)
        print("\tRunning oasdiff command:")
        print(f"\t\t{command}")
        try:
            process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"Failed to run oasdiff command: {command}")
            raise e
        except "failed to load" in process.stderr and "no such file or directory" in process.stderr:
            raise Exception(f"Failed to load file. This might be an issue where schema files are stored separately, like https://github.com/api-extraction-examples/cve-services/blob/f8f2fb7fcab81b0ce507136df6117734c3d0f49d/api-docs/openapi.json#L1078")
        except:
            raise
        stdout = process.stdout.decode('utf-8')
        stderr = process.stderr.decode('utf-8')
        if stdout == "":
            raise Exception(f"{self.owner}/{self.repo_name}: oasdiff failed. \n\tCommand: {command}\n\tStderr: {stderr}")
        if "failed to load base spec from" in stderr and "no such file or directory" in stderr:
            raise Exception(f"Failure to load base spec from local file reference. Error: {stderr}")
        if "failed to load base spec" in stderr and "with error converting YAML to JSON" in stderr:
            raise Exception("Failed to load base spec. Error: {}".format(stderr))
        if "OpenAPI output validation failed" in stderr:
            raise Exception("OpenAPI output validation failed. Error: {}".format(stderr))
        # read bytes from stdout to oasdiff_str
        oasdiff_str = process.stdout.decode('utf-8')
        with open(self.local_oasdiff_file, 'a') as oasdiff_output_file:
            for line in oasdiff_str.splitlines():
                v = ['?', ':']
                for k in v:
                    if line.lstrip().startswith(k):
                        if "method" in line:
                            line = line.replace(k, '-', 1)
                        elif "tags" in line:
                            line = line.replace(k, ' ', 1)
                        else:
                            line = line.replace(k, ' ', 1)
                            print("Potentially mishandling line:", line)
                oasdiff_output_file.write(f"{line}\n")
        # Read the oasdiff file using read_oasdiff_yaml_file and return the output
        oasdiff_output = OasdiffOutput.from_yaml(
            file_path=self.local_oasdiff_file,
            repository_url=self.repo,
            subdirectory=self.subdirectory,
            provided_swagger_file=self.swagger_file,
            new_swagger_file=self.local_revision_swagger_file,
            language=self.language,
            elapsed_time=elapsed_time,
            github_stars=self.github_stars,
            exclude_paths=self.exclude_paths,
        )
        return oasdiff_output


class JobsContainer:
    def __init__(self):
        self.jobs = {}

    def __repr__(self):
        return f"JobsContainer(jobs={len(self.jobs)})"

    def add_job(self, job: Job):
        self.jobs[job.name] = job

    def get_job(self, name):
        return self.jobs.get(name)

    def get_unique_names(self):
        return list(self.jobs.keys())

    def __iter__(self):
        return iter(self.jobs.values())

    def __len__(self):
        return len(self.jobs)

    def __getitem__(self, key):
        # Convert the jobs dictionary to a list of jobs
        jobs_list = list(self.jobs.values())
        # Support slicing
        return JobsContainer.from_list(jobs_list[key])

    @classmethod
    def from_list(cls, jobs_list):
        container = cls()
        for job in jobs_list:
            container.add_job(job)
        return container


# Function to read the YAML file and extract jobs
def read_jobs_from_yaml(file_path: str) -> JobsContainer:
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        container = JobsContainer()
        for job_name, job_details in data['apps'].items():
            repo = job_details['repo']
            swagger_file = job_details['provided_swagger_file']
            language = job_details['language']
            github_stars = job_details['github_stars']
            subdirectory = job_details.get('subdirectory', None)
            include_path_params = job_details.get('include_path_params', False)
            exclude_paths = job_details.get('exclude_paths', None)
            use_config = job_details.get('use_config', None)
            job = Job(
                job_name, repo, swagger_file, language, github_stars, subdirectory, include_path_params, exclude_paths, use_config
            )
            container.add_job(job)
        return container


# Usage example
if __name__ == "__main__":
    workflow_file = join(dirname(__file__), pardir, pardir, ".github", "workflows", "extract-apis.yml")
    jobs_container = read_jobs_from_yaml(workflow_file)

    for job in jobs_container:
        if job.name != "javaspringvulny":
            continue
        print(f"Working on Job: {job.name}")

        # Print job details
        print(f"Repo: {job.repo}, Swagger File: {job.swagger_file}, language: {job.language}")
        print(f"Owner: {job.owner}, Repo Name: {job.repo_name}")

        # Clone the repository
        print("Cloning repository...")
        try:
            job.clone()
        except subprocess.CalledProcessError:
            print("Failed to clone repository. Cleaning it, then run again please")
            job.clean()
            continue

        # Download the base Swagger file
        print("Downloading base Swagger file...")
        job.download_base_swagger()
        start_time = time.time()
        # Run the extraction process
        print("Running extraction...")
        job.run_extraction()
        end_time = time.time()
        elapsed = end_time - start_time
        # Perform OASDiff operation
        print("Performing OASDiff operation...")
        job.oasdiff(elapsed_time=elapsed)

        # Clean up the repository
        print("Cleaning up...")
        job.clean()

        print(f"Completed work on Job: {job.name}\n")

    # # Example usage of JobsContainer
    # for job in jobs_container:
    #     print(f"Job Name: {job.name}, Repo: {job.repo}, Swagger File: {job.swagger_file}, language: {job.language}")
    #
    # # Get a specific job
    # specific_job = jobs_container.get_job("javaspringvulny")
    # if specific_job:
    #     print(f"Specific Job - Repo: {specific_job.repo}")
    #
    # # List unique job names
    # print("Unique Job Names:", jobs_container.get_unique_names())
