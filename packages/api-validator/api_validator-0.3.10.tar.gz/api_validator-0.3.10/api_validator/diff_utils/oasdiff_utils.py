import yaml
import fnmatch

from typing import List


def get_endpoint_method_pairs_from_openapi(file_content) -> List[tuple]:
    """
    Parse the OpenAPI data and return a list of endpoints
    """
    openapi_spec = yaml.safe_load(file_content)

    endpoints = []
    # TODO: This doesn't consider parameters
    for path, path_item in openapi_spec.get('paths', {}).items():
        for method in path_item:
            if method.lower().startswith('x-'):
                continue
            endpoints.append((method.upper(), path))

    # sort them by path, then method
    endpoints = sorted(endpoints, key=lambda x: (x[1], x[0]))
    return endpoints


def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def find_unique_endpoints(original_list: List[tuple], new_list: List[tuple]):
    """
    Find the unique endpoints
    """
    # Convert lists to sets of tuples for efficient comparison
    original_set = set(original_list)
    new_set = set(new_list)

    # Find elements in the new set that are not in the original set
    unique_to_new_set = new_set - original_set

    # Convert back to a list of tuples if needed
    unique_to_new_list = list(unique_to_new_set)

    # sort them by path, then method
    unique_to_new_list = sorted(unique_to_new_list, key=lambda x: (x[1], x[0]))
    return unique_to_new_list


def exclude_endpoints(endpoints: List[str], exclusions: List[str]) -> List[str]:
    result = []

    for endpoint in endpoints:
        exclude = False

        # Check if the endpoint matches any of the exclusion patterns
        for exclusion in exclusions:
            if fnmatch.fnmatch(endpoint, exclusion):
                exclude = True
                break

        if not exclude:
            result.append(endpoint)
    return result


def match_exclusions(endpoints: List[str], exclusions: List[str]) -> List[str]:
    result = []
    if not exclusions:
        return result
    for endpoint in endpoints:
        match = False

        # Check if the endpoint matches any of the exclusion patterns
        for exclusion in exclusions:
            if fnmatch.fnmatch(endpoint, exclusion):
                match = True
                break

        if match:
            result.append(endpoint)

    return result
