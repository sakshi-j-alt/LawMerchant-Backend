# your_app_name/utils.py
import json
import os

def load_json_data():
    json_file_path = os.path.join(os.path.dirname(__file__), 'dummy_regulations.json')
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data
