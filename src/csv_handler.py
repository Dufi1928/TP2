#import csv

def read_csv_file(file_path: str) => list:
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            return [row for row in reader]
    except FileNotFoundError:
        return []

def write_csv_file(file_path: str, data: list) -> none:
    with open(file_path, 'w') as file:
        writer = csv.writer(file)
        writer.writerows(data)
