import csv
import json

def parse_csv_and_save_as_json(input_file, output_file):
    output_list = []
    skip_count = 0

    # Read the CSV file
    with open(input_file, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            try:
                if row[5] == "American Scenes":
                            json_data = json.loads(row[12])
                            if isinstance(json_data, dict):  # Check if it's a dictionary
                                for value in json_data.values():
                                    output_list.append(value)  # Add each value to the list
                            else:
                                print("JSON data in row is not in expected format:", json_data)
            except json.JSONDecodeError:
                print(f"Error parsing JSON in row: {row}")

    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(output_list, jsonfile, indent=4)

input_csv_file = "postcard-tag-old-classifications.csv"  # Replace with your input CSV file path
output_json_file = "american_classify_file_name.json"  # Replace with the desired output JSON file path

parse_csv_and_save_as_json(input_csv_file, output_json_file)