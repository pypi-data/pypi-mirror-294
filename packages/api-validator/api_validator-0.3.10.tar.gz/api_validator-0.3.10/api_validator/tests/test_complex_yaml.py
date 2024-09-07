import unittest
import yaml
import json
from os.path import join, dirname
from api_validator.diff_utils.complex_oasdiff_yaml_utils import transform_complex_keys, OasdiffFile


class TestComplexYaml(unittest.TestCase):
    def test_complex_yaml(self):
        lines = [
            "?   method: GET",
            "    path: /api/v4/users/{id}/following",
            ":   extensions:",
            "        added:",
            "            - x-name",
            "            - x-source"
        ]

        transformed_lines = transform_complex_keys(lines, 0, 2)
        content = "\n".join(transformed_lines)
        print(content)
        # Read it as yaml to make sure it is legit
        data = yaml.safe_load(content)
        print(json.dumps(data, indent=4))
        expected = {
            "{\"method\": \"GET\", \"path\": \"/api/v4/users/{id}/following\"}": {
                "extensions": {
                    "added": [
                        "x-name",
                        "x-source"
                    ]
                }
            }
        }
        self.assertEqual(data, expected)
        # for line in transformed_lines:
        #     print(line)

    def test_oasdiff_file_small(self):
        lines = [
            "?   method: GET",
            "    path: /api/v4/users/{id}/following",
            ":   extensions:",
            "        added:",
            "            - x-name",
            "            - x-source",
            "",
            "?   method: DELETE",
            "    path: /api/v4/projects/{id}",
            ":   extensions:",
            "        added:",
            "            - x-header"
        ]

        content = "\n".join(lines)
        # Initialize the transformer
        transformer = OasdiffFile(content)

        # Apply transformations
        transformer.apply_transformations()

        # Get the transformed lines
        transformed_lines = transformer.transform_lines()

        # Print the result
        print(json.dumps(transformed_lines, indent=4))
        expected = [
            "",
            "\"{\\\"method\\\": \\\"GET\\\", \\\"path\\\": \\\"/api/v4/users/{id}/following\\\"}\":",
            "  extensions:",
            "        added:",
            "            - x-name",
            "            - x-source",
            "",
            "",
            "\"{\\\"method\\\": \\\"DELETE\\\", \\\"path\\\": \\\"/api/v4/projects/{id}\\\"}\":",
            "  extensions:",
            "        added:",
            "            - x-header"
        ]
        self.assertListEqual(transformed_lines, expected)
        # Show that it can be read into yaml without error
        data = yaml.safe_load("\n".join(transformed_lines))
        expected = {
            "{\"method\": \"GET\", \"path\": \"/api/v4/users/{id}/following\"}": {
                "extensions": {
                    "added": [
                        "x-name",
                        "x-source"
                    ]
                }
            },
            "{\"method\": \"DELETE\", \"path\": \"/api/v4/projects/{id}\"}": {
                "extensions": {
                    "added": [
                        "x-header"
                    ]
                }
            }
        }
        print(json.dumps(data, indent=4))
        self.assertDictEqual(data, expected)

    def test_oasdiff_file_gitlab(self):
        with open(join(dirname(__file__), "oasdiff_files", "gitlab-oasdiff-v2.yml"), "r") as f:
            content = f.read()
        transformer = OasdiffFile(content)
        transformer.apply_transformations()
        transformed_lines = transformer.transform_lines()

        # Show that it can be read into yaml without raising an exception
        data = yaml.safe_load("\n".join(transformed_lines))
        # print(json.dumps(data, indent=4))

    def test_gitlab_case_2(self):
        content = """        ?   method: PATCH
            path: /api/v4/projects/{id}/job_token_scope
        :   extensions:
                added:
                    - x-name
                    - x-source
                deleted:
                    - x-codegen-request-body-name"""
        transformer = OasdiffFile(content)
        transformer.apply_transformations()
        transformed_lines = transformer.transform_lines()
        # Show that it can be read into yaml without error. It will raise an exception if it doesn't work.
        data = yaml.safe_load("\n".join(transformed_lines))
        # print(json.dumps(data, indent=4))
