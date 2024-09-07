import unittest
from os.path import join, pardir, dirname, exists
import json
from api_validator.diff_utils.oasdiff_utils import get_endpoint_method_pairs_from_openapi, read_file, find_unique_endpoints, exclude_endpoints, match_exclusions


class TestSwaggerUtils(unittest.TestCase):
    def setUp(self):
        self.swagger_file = join(dirname(__file__), "oasdiff_files", "cert-viewer-revision.yml")

    def test_get_endpoint_method_pairs_from_openapi(self):
        """
        Test that we can parse the OpenAPI data
        """
        file_content = read_file(self.swagger_file)
        endpoints = get_endpoint_method_pairs_from_openapi(file_content)
        self.assertEqual(len(endpoints), 33)
        self.assertEqual(endpoints[0], ('GET', '/'))

    def test_find_unique_endpoints(self):
        file_content = read_file(self.swagger_file)
        base_endpoints = get_endpoint_method_pairs_from_openapi(file_content)
        new_endpoints = [('GET', '/fake1'), ('GET', '/fake2'), ('GET', '/{certificate_uid}')]
        unique_endpoints = find_unique_endpoints(base_endpoints, new_endpoints)
        expected = [('GET', '/fake1'), ('GET', '/fake2')]
        self.assertEqual(unique_endpoints, expected)

    def test_excluded_endpoints(self):
        # Example usage:
        endpoints = [
            'path_a',
            'prefix_path/nested/should_be_excluded',
            'prefix-wildcard-should-be-excluded',
            'example-suffix',
            'path_b',
            'some_prefix/nested',
            'some_prefix',
        ]

        exclusions = [
            'path_a',
            'prefix_path/*',
            'prefix*',
            '*suffix',
        ]

        filtered_endpoints = exclude_endpoints(endpoints, exclusions)
        expected = ['path_b', 'some_prefix/nested', 'some_prefix']
        self.assertListEqual(filtered_endpoints, expected)

    def test_match_exclusions(self):
        # Example usage:
        endpoints = [
            'path_a',
            'prefix_path/nested/should_be_excluded',
            'prefix-wildcard-should-be-excluded',
            'example-suffix',
            'path_b',
            'some_prefix/nested',
            'some_prefix',
        ]

        exclusions = [
            'path_a',
            'prefix_path/*',
            'prefix*',
            '*suffix',
        ]

        matching_endpoints = match_exclusions(endpoints, exclusions)
        expected = ['path_a', 'prefix_path/nested/should_be_excluded', 'prefix-wildcard-should-be-excluded', 'example-suffix']
        self.assertListEqual(matching_endpoints, expected)
