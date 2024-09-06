#!/usr/bin/env python3
import csv
from os.path import join, dirname, isdir, exists, isfile, basename
from os import listdir, remove
from pathlib import Path


def combine_newman_csv(output_file: str, artifact_directory: str):
    """Combine Newman CSV files into one CSV file."""
    # The artifact directory will contain a lot of subfolders prefixed with `newman-{app_name}`. Each of these
    # subfolders will contain a `newman.csv` file. We want to combine all of these `newman.csv` files into one CSV
    # file, and prepend the app_name as the first column. The first row of the CSV file should be the column names.
    # Initialize a list to store the combined data
    combined_data = []

    keys_to_delete = ["iteration", "collectionName"]
    # keys_to_delete = ["iteration", "collectionName", "totalAssertions", "executedCount", "failedCount",
    # "skippedCount"] field_names = ["app_name", "url", "method", "code", "status", "requestName", "responseTime",
    # "responseSize", "executed", "failed", "skipped"]
    field_names = ["app_name", "url", "method", "code", "status", "requestName", "responseTime", "responseSize", "executed", "failed", "skipped", "totalAssertions", "executedCount", "failedCount", "skippedCount"]
    # Iterate through the subdirectories in the artifact directory
    for sub in listdir(artifact_directory):
        if isfile(join(artifact_directory, sub)) and sub.endswith('.csv'):
            app_name = Path(sub).stem
            csv_file_path = join(artifact_directory, sub)

            with open(csv_file_path, 'r', newline='') as csvfile:
                # Read the CSV data from 'newman.csv' into a list of dictionaries
                reader = csv.DictReader(csvfile)

                # Modify each row dictionary to include the 'app_name' key and value
                for row in reader:
                    row_data: dict = row
                    for key in keys_to_delete:
                        if key not in field_names:
                            row_data.pop(key, None)
                    row_data["app_name"] = app_name
                    combined_data.append(row_data)

    if exists(output_file):
        print(f"Output file '{output_file}' already exists. Overwriting...")
        remove(output_file)
    # Write the combined data to the output CSV file
    with open(output_file, 'w') as output_file:
        writer = csv.DictWriter(f=output_file, fieldnames=field_names)
        writer.writeheader()
        # Write the combined data along with column names as the first row
        if combined_data:
            # Move app_name, url, status, code, and requestName to the front
            # move_to_front = ["app_name", "url", "status", "code", "requestName"]
            #
            # fieldnames = move_to_front + [key for key in fieldnames if key not in move_to_front]
            for row in combined_data:
                writer.writerow(row)


