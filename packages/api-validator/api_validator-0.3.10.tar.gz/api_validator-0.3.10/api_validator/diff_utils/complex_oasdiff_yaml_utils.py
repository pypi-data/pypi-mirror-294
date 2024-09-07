from typing import List
import yaml
import re


def transform_complex_keys(lines: List[str], start_line: int, end_line: int) -> List[str]:
    """
    Transforms complex keys into a string representation of a dict.

    Args:
        lines: A list of lines in the file.
        start_line: The line with the "?" (starting index).
        end_line: The line with the section block (e.g., extensions: or tags:).

    Returns:
        List of lines with the transformation applied.
    """
    # # Capture leading spaces (indentation) for the line with the "?"
    # leading_spaces = len(lines[start_line]) - len(lines[start_line].lstrip())
    #
    # # Extract the method and path
    # method_line = lines[start_line].replace("?", "").strip()


    # Capture leading spaces (indentation) for the line with the "?"
    leading_spaces = len(lines[start_line]) - len(lines[start_line].lstrip())

    # Check if the line contains both method and path or just a path
    method_line = lines[start_line].replace("?", "").strip()

    if method_line.startswith("method:"):  # Case with method and path
        # Extract the method and path
        method = method_line.split(": ")[1]
        path = lines[start_line + 1].strip().split(": ")[1]

        # Escape backslashes in the path (e.g., for cases like \(\))
        path = path.replace('\\', '\\\\')

        # Combine method and path into a string representation of a dict (as a valid YAML key)
        dict_key = f'"{{\\"method\\": \\"{method}\\", \\"path\\": \\"{path}\\"}}":'
        lines[start_line] = ' ' * leading_spaces  # Replace start_line with just spaces
        lines[start_line + 1] = ' ' * leading_spaces + dict_key

    else:  # Case with just a path
        path = method_line.split(": ")[1] if ": " in method_line else method_line
        path = path.replace('\\', '\\\\')  # Escape backslashes

        # Use only the path as the key
        dict_key = f'"{{\\"path\\": \\"{path}\\"}}":'
        lines[start_line] = ' ' * leading_spaces + dict_key

    # Ensure the indentation of the block following the key (end_line)
    # Align the section block (like 'operations', 'extensions', or 'tags') correctly
    end_line_leading_spaces = len(lines[end_line]) - len(lines[end_line].lstrip())
    if lines[end_line].lstrip().startswith(':'):
        # lines[end_line] = ' ' * leading_spaces + lines[end_line].lstrip().replace(':', '', 1).strip()
        lines[end_line] = "  " + ' ' * end_line_leading_spaces + lines[end_line].lstrip().replace(':', '', 1).strip()

    return lines

    # path_line = lines[start_line + 1].strip()
    #
    # # Escape backslashes in the path_line (especially for cases like \(\))
    # path_line = path_line.replace('\\', '\\\\')
    #
    # # Combine method and path into a string representation of a dict (as a valid YAML key)
    # dict_key = f'"{{\\"method\\": \\"{method_line.split(": ")[1]}\\", \\"path\\": \\"{path_line.split(": ")[1]}\\"}}":'
    #
    # # Add back the leading spaces and replace the lines with the transformed key
    # lines[start_line] = ' ' * leading_spaces  # Replacing start_line with just spaces
    # lines[start_line + 1] = ' ' * leading_spaces + dict_key
    #
    # # Capture the leading spaces for the section line (end_line)
    # end_line_leading_spaces = len(lines[end_line]) - len(lines[end_line].lstrip())
    #
    # # Add a tab before the section line (like 'extensions' or 'tags') and remove the initial colon
    # if lines[end_line].lstrip().startswith(':'):
    #     lines[end_line] = "    " + ' ' * end_line_leading_spaces + lines[end_line].lstrip().replace(':', '', 1).strip()
    #
    # return lines


class OasdiffFile:
    def __init__(self, content: str):
        """
        Initialize the class with the lines from the file.
        """
        self.content = content
        self.lines = content.splitlines()

    def detect_complex_key_blocks(self) -> List[tuple]:
        """
        Detects the start and end lines of complex key blocks.

        Returns:
            A list of tuples, where each tuple contains (start_line, end_line).
        """
        complex_key_blocks = []
        pattern_start = re.compile(r'^\s*\?\s+method:')  # Allow for any leading spaces before `? method`
        pattern_end = re.compile(
            r'^\s*:\s+(extensions|tags):')  # Generalized detection for sections like extensions or tags

        start_line = None

        for i, line in enumerate(self.lines):
            # Detect the start of the block
            if pattern_start.match(line):
                start_line = i

            # Detect the end of the block and store the range
            if start_line is not None and pattern_end.match(line):
                end_line = i
                complex_key_blocks.append((start_line, end_line))
                start_line = None  # Reset for the next block

        return complex_key_blocks

    def apply_transformations(self):
        """
        Applies the transform_complex_keys function to each detected block
        and replaces the corresponding lines in the instance variable `lines`.
        """
        # Detect all blocks
        complex_key_blocks = self.detect_complex_key_blocks()

        for start_line, end_line in complex_key_blocks:
            # Transform the lines for this block
            these_transformed_lines = transform_complex_keys(self.lines, start_line, end_line)

            # Replace the lines in the original lines with the transformed ones
            self.lines[start_line:end_line + 1] = these_transformed_lines[start_line:end_line + 1]
        self.content = "\n".join(self.lines)
        self.fix_block_mapping_errors()
        return self.lines

    def fix_block_mapping_errors(self) -> dict:
        """
        Sometimes, oasdiff has lines that don't have the : at the end, like this

                  /api/v4/projects/{id}/packages/conan/v1/conans/{package_name}/{package_version}/{package_username}/{package_channel}/download_urls
            operations:
                modified:

        This is a dirty hack to fix that.
        :return:
        """
        try:
            data = yaml.safe_load(self.content)
        except yaml.YAMLError as exc:
            if hasattr(exc, 'problem_mark') and hasattr(exc, 'problem'):
                if exc.problem == "expected <block end>, but found '<scalar>'":
                    mark = exc.problem_mark
                    # Insert a : at the end of the line
                    self.lines[mark.line] = self.lines[mark.line] + ":"
                    self.content = "\n".join(self.lines)
                    data = self.fix_block_mapping_errors()
                elif exc.problem == "expected <block end>, but found '<block mapping start>'":
                    mark = exc.problem_mark
                    # Remove one space from the start of the line
                    self.lines[mark.line] = self.lines[mark.line][1:]
                    self.content = "\n".join(self.lines)
                    data = self.fix_block_mapping_errors()
                else:
                    raise exc
            else:
                raise exc
        return data

    def transform_lines(self) -> List[str]:
        """
        Returns the transformed lines.
        """
        return self.lines

    def get_transformed_content(self) -> str:
        """
        Returns the transformed content as a string.
        """
        return "\n".join(self.lines)

    def dict(self):
        data = yaml.safe_load(self.content)
        return data


def example_transform_complex_keys():
    # Example usage
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

    # To make sure it parses as YAML
    data = yaml.safe_load(content)
    print(data)


def example_oasdiff_file():
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
    print("\n".join(transformed_lines))


if __name__ == '__main__':
    example_oasdiff_file()
