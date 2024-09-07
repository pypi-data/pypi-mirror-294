from os.path import join, dirname, exists, abspath, expanduser


def validate_internal_binary_path(binary_path: str):
    """Validate the path to the internal API Extractor binary."""
    if binary_path:
        binary_path = expanduser(binary_path)
        if not exists(binary_path):
            raise FileNotFoundError(f"API Extractor binary not found at {binary_path}")
        print(f"--binary-path set to {binary_path}")
    if not binary_path:
        if exists(join(dirname(__file__), "api-excavator")):
            binary_path = abspath(join(dirname(__file__), "api-excavator"))
        else:
            binary_path = "api-excavator"
    return binary_path
