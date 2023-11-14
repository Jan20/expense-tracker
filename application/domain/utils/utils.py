import csv

def read_csv_file(file_path: str):
    """
    Reads a CSV file and returns the data as a list of dictionaries.

    Parameters:
    - file_path (str): The path to the CSV file.

    Returns:
    - list of dict: A list of dictionaries where each dictionary represents a row in the CSV file.
    """
    data = []
    with open(file_path, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return data
