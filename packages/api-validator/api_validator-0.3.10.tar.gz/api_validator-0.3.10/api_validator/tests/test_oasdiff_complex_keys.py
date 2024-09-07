import unittest

from os.path import join, dirname
import unittest
from pathlib import Path
import json
import yaml

from api_validator.tools.oasdiff import OasdiffOutput, read_oasdiff_yaml_file, preprocess_yaml
from api_validator.diff_utils.job_summary import GitHubJobSummary


class TestOasdiffOutput(unittest.TestCase):
  #   def test_complex_keys(self):
  #       example = """modified:
  # ?
  #   method: GET
  #   path: /api/v4/projects/{id}/packages/conan/v1/conans/{package_name}/{package_version}/{package_username}/{package_channel}/download_urls
  # :
  #   extensions:"""
  #       data = read_oasdiff_yaml_string(example)
  #       # # Add custom constructor for unhashable keys
  #       # yaml.add_constructor(
  #       #     yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
  #       #     construct_mapping,
  #       #     Loader=yaml.UnsafeLoader
  #       # )
  #       #
  #       # # Load YAML data with the custom loader
  #       # data = yaml.load(example, Loader=yaml.UnsafeLoader)
  #       # data_with_string_keys = convert_keys_to_strings(data)
  #
  #       # Print the output to verify the structure
  #       for key, value in data.items():
  #           print("Key:", key)
  #           print("Value:", value)
  #
  #       # Output the data as JSON for easy readability
  #       print(json.dumps(data, indent=4))
  #       expected = {
  #           "modified": {
  #               "(('method', 'GET'), ('path', '/api/v4/projects/{id}/packages/conan/v1/conans/{package_name}/{package_version}/{package_username}/{package_channel}/download_urls'))": {
  #                   "extensions": None
  #               }
  #           }
  #       }
  #       self.assertDictEqual(data, expected)

    # TODO: We can just send any non-friendly OpenaPI files to the Swagger conversion API - https://converter.swagger.io/
    # def test_gitlab_v2_complex_keys(self):
    #     gitlab_file = join(dirname(__file__), "oasdiff_files", "gitlab-complex-keys.yml")
    #     gitlab_revision = ""
    #     gitlab_provided = ""
    #     gitlab_diff = OasdiffOutput.from_yaml(
    #         gitlab_file,
    #         repository_url="https://gitlab.com/gitlab-org/gitlab/",
    #         new_swagger_file=gitlab_revision,
    #         provided_swagger_file=gitlab_provided,
    #         language="ruby",
    #         elapsed_time=20.0,
    #     )
    #     job_summary = GitHubJobSummary([gitlab_diff], overall_elapsed_time=60)
    #     step_summary = job_summary.github_step_summary()
    #     print(step_summary)

    def test_gitlab_v2(self):
        gitlab_file = join(dirname(__file__), "oasdiff_files/oasdiff-gitlab.yml")
        gitlab_revision = join(dirname(__file__), "oasdiff_files/gitlab-v2-revision.yml")
        gitlab_provided = join(dirname(__file__), "oasdiff_files/gitlab-v2-base.yml")
        gitlab_diff = OasdiffOutput.from_yaml(
            gitlab_file,
            repository_url="https://gitlab.com/gitlab-org/gitlab/",
            new_swagger_file=gitlab_revision,
            provided_swagger_file=gitlab_provided,
            language="ruby",
            elapsed_time=20.0,
        )
        job_summary = GitHubJobSummary([gitlab_diff], overall_elapsed_time=60)
        step_summary = job_summary.github_step_summary()
        print(step_summary)

    def test_gitlab_v3(self):
        gitlab_file = join(dirname(__file__), "oasdiff_files/gitlab-oasdiff-v2.yml")
        gitlab_revision = join(dirname(__file__), "oasdiff_files/gitlab-v3-revision.yaml")
        gitlab_provided = join(dirname(__file__), "oasdiff_files/gitlab-v2-base.yml")
        gitlab_diff = OasdiffOutput.from_yaml(
            gitlab_file,
            repository_url="https://gitlab.com/gitlab-org/gitlab/",
            new_swagger_file=gitlab_revision,
            provided_swagger_file=gitlab_provided,
            language="ruby",
            elapsed_time=20.0,
        )
        job_summary = GitHubJobSummary([gitlab_diff], overall_elapsed_time=60)
        step_summary = job_summary.github_step_summary()
        print(step_summary)
