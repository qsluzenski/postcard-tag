import json
import csv

json_file_path1 = "transcribe_file_name.json"
json_file_path2 = "transcribe_result.json"
output_file_path = "transcribe_merged_output.json"  # Specify the desired output file path
csv_file_path = "transcribe_merged.csv"

# Load content from JSON files
with open(json_file_path1, "r") as file1, open(json_file_path2, "r") as file2:
    data1 = json.load(file1)
    data2 = json.load(file2)

# Merge dictionaries
merged_data = []

# Iterate through the dictionaries in both lists
for dict1, dict2 in zip(data1, data2):
    merged_dict = {}
    
    # Update with the content from the first JSON file
    for key, value in dict1.items():
        merged_dict[key] = value
    
    # Update with the content from the second JSON file
    for key, value in dict2.items():
        merged_dict[key] = value
    
    merged_data.append(merged_dict)

# Write merged data to a new JSON file
with open(output_file_path, "w") as output_file:
    json.dump(merged_data, output_file, indent=4)

print("Merged data written to", output_file_path)


# Load content from JSON file
with open(output_file_path, "r") as json_file:
    data = json.load(json_file)

header = ["retired", "Other size file name", "Other side file name", "Handwriting file name", "# Parent unique identifier", "#Parent unique identifier", "#Handwriting unique identifier", "T5", "T6", "Language"]


# Write JSON data to CSV
with open(csv_file_path, "w", newline="") as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=header)
    
    # Write the header row
    csv_writer.writeheader()
    
    # Write each dictionary as a row in the CSV file
    for entry in data:
        if entry["retired"] is not None:  # Only write if "retired" is not null
            csv_writer.writerow(entry)

print("JSON data converted to CSV:", csv_file_path)