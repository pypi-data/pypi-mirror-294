import argparse
import json
import sys

import yaml
from typing import Any, Dict, List, Optional


def update_server_info(data: Dict[str, Any], url: str, description: str) -> None:
    if 'servers' in data:
        for server in data['servers']:
            server['url'] = url
            server['description'] = description


def add_server_entry_to_swagger_file(file_path: str, output_file: str, url: str, description: str) -> None:
    # Validate that the output file ends in yaml/yml
    if output_file is not None and not output_file.endswith('.yaml') and not output_file.endswith('.yml'):
        print("Output file must end in yaml/yml")
        sys.exit(1)

    with open(file_path, 'r') as file:
        try:
            if file_path.endswith('.json'):
                data = json.load(file)
            elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
                data = yaml.safe_load(file)
            else:
                print(f"Unsupported file format: {file_path}")
                return
        except Exception as e:
            print(f"Error reading file {file_path}: {str(e)}")
            return

    update_server_info(data, url, description)

    with open(output_file, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)
        # if file_path.endswith('.json'):
        #     json.dump(data, file, indent=2)
        # elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
        #     yaml.dump(data, file, default_flow_style=False)
