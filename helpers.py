import os
import csv
import json
import gridly_api_calls
from collections import defaultdict
from classes import methodResponse


def create_columns_if_not_exists(viewId, apiKey, view, json_languages, sourcelanguage):
    language_codes = []
    added_langs = []
    view = gridly_api_calls.get_view(viewId, apiKey)
    for column in view["columns"]:
        if "languageCode" in column:
            language_codes.append(column["languageCode"])
    print(language_codes)
    if sourcelanguage not in language_codes:
        gridly_api_calls.create_column(viewId, apiKey, sourcelanguage, "sourceLanguage")
        added_langs.append(sourcelanguage)
    for lang in json_languages:
        if lang in added_langs:
            continue
        if lang not in language_codes:
            if lang == sourcelanguage:
                gridly_api_calls.create_column(viewId, apiKey, lang, "sourceLanguage")
            else:
                gridly_api_calls.create_column(viewId, apiKey, lang, "targetLanguage")
            if sourcelanguage != None:
                dependencies = gridly_api_calls.get_dependencies(viewId, apiKey)
                if any(item['sourceColumnId'] == sourcelanguage and item['targetColumnId'] == lang for item in dependencies) == False:
                    if lang != sourcelanguage:
                        gridly_api_calls.create_dependency(viewId, apiKey, sourcelanguage, lang)
                           


def convert_json_into_records(rootPath, filepath, viewId, apiKey, generate_columns, view, sourcelanguage):
    try:
        """
        Processes a JSON file, optionally generating columns based on its content, and returns transformed data.
        
        :param rootPath: Base directory path for computing relative paths.
        :param filepath: Absolute path to the JSON file.
        :param viewId: Identifier for the view where data needs to be processed.
        :param apiKey: API key for accessing the view.
        :param generate_columns: Boolean indicating if new columns need to be created based on JSON keys.
        :param view: View configuration or settings.
        :param sourcelanguage: Source language code used in processing.
        :return: Transformed data from the JSON file.
        """
        # Generate the relative path from rootPath to filepath
        filename = os.path.basename(filepath)
        fpath = os.path.relpath(filepath, rootPath)
        fpath = fpath.replace("\\", "/")  # Ensuring the path uses forward slashes

        # Load JSON data from the file
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Optional column generation based on JSON keys
        if generate_columns:
            language_codes = list(data.keys())
            create_columns_if_not_exists(viewId, apiKey, view, language_codes, sourcelanguage)

        # Process and transform the JSON data
        return transform_i18n_data(data, fpath, filename, filepath)
    except Exception as e:
        return {"type": "ERROR", "message": str(e), "filePath": filepath}

def transform_i18n_data(data, filePath, fileName, fullPath):
    try:
        def recurse_items(current_data, path=[]):
            if isinstance(current_data, dict):
                for key, value in current_data.items():
                    # Continue diving if the value is still a dictionary
                    if isinstance(value, dict):
                        yield from recurse_items(value, path + [key])
                    else:
                        # Reached a leaf node, yield path and value
                        yield path + [key], value
            else:
                # Reached a leaf node in a non-dict context (unlikely in given JSON structure)
                yield path, current_data

        # Prepare the output list
        output = []
        # Mapping of paths to their respective entries in the output list
        path_to_entry_index = {}

        # Iterate over all languages and their respective data
        for lang, contents in data.items():
            # Get all paths and values using the recursive function
            for path, value in recurse_items(contents):
                # Convert path to a string ID
                id_str = fileName + "_¤_" + "_¤_".join(path)
                if id_str not in path_to_entry_index:
                    # Create a new entry if this path has not been added to output yet
                    path_to_entry_index[id_str] = len(output)
                    output.append({"id": id_str, "cells": [], "path": filePath})
                # Append the cell for the current language
                output[path_to_entry_index[id_str]]["cells"].append({"value": value, "columnId": lang})
        #print(output)
        return {"type": "OK", "records": output, "filePath": fullPath, "numOfRecords": len(output)}
    except Exception as e:
        # Handle any kind of exception, return an error message
        return {"type": "ERROR", "message": str(e), "filePath": filePath}


def export_into_i18n_json(root_path, viewId, apiKey):
    response = methodResponse("exportResponse")
    try:
        csv_data = gridly_api_calls.export_view_as_csv(viewId, apiKey)
        reader = csv.reader(csv_data.splitlines())

        try:
            header = next(reader)
        except StopIteration:
            raise ValueError("CSV data is empty or headers are missing")

        if len(header) < 4:
            raise ValueError("Insufficient columns in CSV header")

        languages = header[2:]  # Assume language columns start from the third column
        json_files = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
        row_counts = defaultdict(int)

        for row in reader:
            if len(row) < len(languages) + 2:
                print("Skipping malformed row:", row)
                continue

            relative_path, record_id = row[:2]
            full_path = os.path.join(root_path, relative_path)  # Combine with root path
            # Remove filename part and leading delimiter
            keys = record_id.split("_¤_")[1:]  # Skip the first element (filename and delimiter)

            if not keys:
                continue

            row_counts[full_path] += 1  # Increment row count for this path

            # Build nested dictionary structure
            for lang_index, lang in enumerate(languages):
                current_level = json_files[full_path][lang]
                for key in keys[:-1]:
                    if key not in current_level:
                        current_level[key] = {}
                    current_level = current_level[key]
                current_level[keys[-1]] = row[lang_index + 2]  # Assign translation

        # Save each dictionary to its corresponding JSON file
        for path, translations in json_files.items():
            os.makedirs(os.path.dirname(path), exist_ok=True)  # Ensure directory exists
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(translations, f, ensure_ascii=False, indent=2)
            #print(f"JSON data has been saved to '{path}'")
            response.add_successful_file(path, row_counts[path])

    except Exception as e:
        response.add_failed_file(path, str(e))

    finally:
        json_output = response.generate_json()
        print(json_output)
