#!/usr/bin/env python3
"""
We are hitting an issue with nodejs-goof where newman is sending a request to the /destroy` endpoint which is causing the app to crash, so we can't run the rest of the newman validation.

To work around this, we are applying a workaround where we add a prerequest script to the newman collection to exclude the /destroy endpoint from the collection run.

Basically, it will loop through every item under the `item` key in the collection, and if the name equals what is in the config, it will look for the corresponding GET/POST/PUT and add a prerequest script by adding the following event:

"event": [
    {
        "listen": "prerequest",
        "script": {
            "exec": [
                "pm.execution.skipRequest()"
            ],
            "type": "text/javascript"
        }
    }
],
"""
import json
import os.path

import yaml
from os.path import dirname, join
import click


def read_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def modify_item_v2(item: dict, skip_endpoints: list):
    # Check if the item is a request (not a folder)
    if item.get("request"):
        for skip_endpoint in skip_endpoints:
            path = '/'.join(item["request"]["url"]["path"])
            method = item["request"]["method"].upper()
            if path == skip_endpoint['path'] and method == skip_endpoint['method'].upper():
                if "event" not in item:
                    item["event"] = []
                print(f"Adding prerequest script to skip request: {method} /{path}")
                item["event"].append({
                    "listen": "prerequest",
                    "script": {
                        "exec": ["pm.execution.skipRequest()"],
                        "type": "text/javascript"
                    }
                })
    # If the item is a folder, recursively modify its items
    if item.get("item"):
        updated_items = []
        for sub_item in item["item"]:
            updated_sub_item = modify_item_v2(sub_item, skip_endpoints)
            updated_items.append(updated_sub_item)
        item["item"] = updated_items  # Update the item's "item" key with the modified items
    return item  # Return the modified item


def modify_collection_v2(collection: dict, skip_endpoints: list):
    updated_collection = collection.copy()  # Create a copy of the original collection
    updated_items = []
    for item in updated_collection['item']:
        updated_item = modify_item_v2(item, skip_endpoints)
        updated_items.append(updated_item)

    updated_collection['item'] = updated_items  # Update the collection with the modified items
    return updated_collection  # Return the updated collection


def get_paths_from_item_v2(sub_item: dict):
    paths = []
    # Check if the item is a request (not a folder)
    if sub_item.get("request"):
        # path = join the path items with a slash
        path = '/'.join(sub_item["request"]["url"]["path"])
        method = sub_item["request"]["method"].upper()
        data = (path, method)
        paths.append(data)
    # If the item is a folder, recursively modify its items
    elif sub_item.get("item"):
        for sub_sub_item in sub_item["item"]:
            data = get_paths_from_item_v2(sub_sub_item)
            paths.extend(data)
    return paths


def get_paths_v2(collection: dict):
    paths = set()
    for item in collection['item']:
        # Check if the item is a request (not a folder)
        if item.get("request"):
            path = '/'.join(item["request"]["url"]["path"])
            paths.add((path, item.request.method.upper()))  # Convert to tuple to make it hashable
        # If the item is a folder, recursively modify its items
        if item.get("item"):
            for sub_item in item["item"]:
                paths.update(get_paths_from_item_v2(sub_item))
    paths = [{"path": path, "method": method} for path, method in paths]
    paths = list(paths)
    # Sort the list of dictionaries first by "path" and then by "method"
    sorted_paths = sorted(paths, key=lambda x: (x["path"], x["method"]))
    return sorted_paths


def print_paths(collection: dict):
    paths = get_paths_v2(collection)
    print("Printing Paths and methods discovered in the Postman Collection.")
    for path in paths:
        # Print a leading / for readability
        print(f"\t{path['method']} /{path['path']}")


def add_postman_exclusion(output_file: str, collection_file: str, app: str, config_file: str):
    yaml_data = read_yaml(config_file)
    if app not in yaml_data["apps"]:
        print(f"App '{app}' not found in config file '{config_file}'. Skipping...")
        return
    skip_endpoints = yaml_data["apps"][app]['skip_endpoints']
    # For every skip_endpoint, strip the leading /
    for skip_endpoint in skip_endpoints:
        skip_endpoint["path"] = skip_endpoint["path"].lstrip('/')
    collection = read_yaml(collection_file)
    print_paths(collection)
    modified_collection = modify_collection_v2(collection, skip_endpoints)
    # print(json.dumps(modified_collection, indent=4))
    if os.path.exists(output_file):
        print(f"Output file '{output_file}' already exists. Overwriting...")
    with open(output_file, 'w') as file:
        json.dump(modified_collection, file, indent=4)
