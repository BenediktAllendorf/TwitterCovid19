import json
import os
import re

def load_json(path):
    """Load JSON file from path"""
    try:
        with open(path, 'r') as json_file:
            return json.load(json_file)
    except (OSError, IOError):
        raise FileNotFoundError("File not found: {}".format(path))


def find_json_files(folder):
    """Recursively find all json files in folder that end with *{numbers}.json and yield path"""
    file_pattern = r'^.*[0-9]{10,}\.json$'
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in [f for f in filenames if bool(re.compile(file_pattern).match(f))]:
            yield os.path.join(dirpath, filename)