# csv_to_json.py

import csv
import json

def csv_to_json_string(csv_file_path):
    data = []
    try:
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data.append({k.strip(): v for k, v in row.items()})
        return json.dumps(data)
    except Exception as e:
        return f"Une erreur s'est produite : {e}"