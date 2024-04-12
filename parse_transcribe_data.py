import csv
import json
import pandas as pd

input_csv_file = 'postcard-tag-classifications.csv'
file_name_json = 'transcribe_file_name.json'
json_output = 'transcribe_result.json'
just_json_output = 'transcribe_just_json.json'
file_name_json = 'transcribe_file_name.json'
results_json = 'transcribe_result.json'
merged_json_output = 'transcribe_merged_output.json'
csv_output = 'transcribe_merged.csv'
merged_raw_data = 'transcribe_merged.csv'
csv_to_check = 'check.csv'
csv_for_round_two = 'round2.csv'
final_csv = 'transcribe_cortex_ready.csv'


def main():
    save_file_name_data(input_csv_file, file_name_json)
    output_list, just_json = find_task_values(input_csv_file)
    save_dict_to_json(output_list, json_output)
    save_dict_to_json(just_json, just_json_output)
    merge_json(file_name_json, results_json, merged_json_output)
    write_json_to_csv(merged_json_output, csv_output)
    clean_data(merged_raw_data, csv_to_check)
    sort_output(csv_to_check, csv_for_round_two, final_csv)


def save_file_name_data(input_file, file_name_json):
    output_list = []
    skip_count = 0

    # Read the CSV file and pull out the file name information
    with open(input_file, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            try:
                if row[5] == "Transcribe Handwritten Messages":
                        if skip_count >= 3:
                            json_data = json.loads(row[12])
                            if isinstance(json_data, dict):  # Check if it's a dictionary
                                for value in json_data.values():
                                    output_list.append(value)  # Add each value to the list
                            else:
                                print("JSON data in row is not in expected format:", json_data)
                        else:
                            skip_count += 1
            except json.JSONDecodeError:
                print(f"Error parsing JSON in row: {row}")

    with open(file_name_json, 'w', encoding='utf-8') as jsonfile:
        json.dump(output_list, jsonfile, indent=4)


def find_task_values(input_csv_file):
    # We will parse each row and push the results into this list
    output = [] 
    just_json = []
    skip_count = 0
    with open(input_csv_file, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            try:
                if row[5] == "Transcribe Handwritten Messages":
                        if skip_count >= 3: # skip the first three, since that is data from before the final version
                            data_dict = json.loads(row[11]) # Assuming 0-based indexing, so 11 is the 12th column
                            if isinstance(data_dict, list):
                                just_json.append(data_dict)
                                # this is the row's output, which will be pushed into the final list
                                outpObj = {}
                                for i in data_dict:
                                    if i['task'] == 'T4':
                                        for j in i["value"]:
                                            if j['task'] == 'T5' and len(j["value"]) > 0:
                                                outpObj["T5"] = j["value"]
                                            elif j['task'] == 'T7':
                                                for l in j["value"]:
                                                    if "label" in l:
                                                        outpObj["Language"] = l["label"]
                                            elif j['task'] == 'T6' and len(j["value"]) > 0:
                                                outpObj["T6"] = j["value"]
                                output.append(outpObj)
                        else:
                            skip_count += 1
            except json.JSONDecodeError:
                print('json parse FAIL')
                # Move on if JSON parsing fails
                pass
    
    return output, just_json


def save_dict_to_json(data_dict, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)
    print(f'Dictionary has been saved as {json_output}.')


def merge_json(file_name_json, results_json, merged_json_output):

    # Load content from JSON files
    with open(file_name_json, "r", encoding='utf-8') as file1, open(results_json, "r", encoding='utf-8') as file2:
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
    with open(merged_json_output, "w", encoding='utf-8') as output_file:
        json.dump(merged_data, output_file, indent=4)

    print("Merged data written to", merged_json_output)


def write_json_to_csv(merged_json_output, csv_output):

    # Load content from JSON file
    with open(merged_json_output, "r", encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Headers from the two JSON files for the new CSV
    header = ["retired", "Other size file name", "Other side file name", 'Other file name', "Handwriting file name", "# Parent unique identifier", "#Parent unique identifier", '# Parent Compound Object Identifier', "#Handwriting unique identifier", "T5", "T6", "Language"]

    # Write JSON data to CSV
    with open(csv_output, "w", newline="", encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=header)
        
        # Write the header row
        csv_writer.writeheader()
        
        # Write each dictionary as a row in the CSV file
        for entry in data:
            if entry["retired"] is not None:  # Only write if "retired" is not null
                csv_writer.writerow(entry)

    print(f'JSON data converted to CSV: {csv_output}')


def clean_data(merged_raw_data, csv_to_check):

    df = pd.read_csv(merged_raw_data)

    replacement_dict = {
        '[[NONE]]': " ",
        '[[none]]': " ",
        '[[ NONE ]]': " ",
        '[[ none ]]': " ",
        '[[ NONE  ]]': " ",
        '[[NONE ]]': " ",
        '[[  NONE  ]]': " ",
        '[[ None ]]': " ",
    }

    column_name = 'T5'  # Replace with the actual column name

    for index, row in df.iterrows():
        value = row[column_name]
        
        if isinstance(value, str):  # Check if the value is a string
            for old_phrase, new_phrase in replacement_dict.items():
                value = value.replace(old_phrase, new_phrase)
        
        df.at[index, column_name] = value

    column_name_2 = 'T6'  # Replace with the actual column name

    for index, row in df.iterrows():
        value = row[column_name_2]
        
        if isinstance(value, str):  # Check if the value is a string
            for old_phrase, new_phrase in replacement_dict.items():
                value = value.replace(old_phrase, new_phrase)
        
        df.at[index, column_name_2] = value

    df['Parent file name'] = df['Other side file name'].fillna('') + df['Other size file name'].fillna('')
    df['Parent unique identifier'] = df['# Parent unique identifier'].fillna('') + df['#Parent unique identifier'].fillna('')
    df['Unique identifier'] = df['#Handwriting unique identifier']
    df['Parent file name'] = df['Parent file name'].str.replace('.jpg', '.tif')
    df['Handwriting file name'] = df['Handwriting file name'].str.replace('.jpg', '.tif')
    df['Transcription'] = df['T5'].fillna('') + df['T6'].fillna('')

    # Drop the extra columns
    df = df.drop(['retired', 'T5', 'T6', '#Handwriting unique identifier', 'Other size file name', 'Other side file name', '# Parent unique identifier', '#Parent unique identifier'], axis=1)

    # Save the modified DataFrame to a new CSV file
    df.to_csv(csv_to_check, index=False)


def sort_output(csv_to_check, csv_for_round_two, final_csv):

    df = pd.read_csv(csv_to_check)

    # Define the value to check for in the column
    value_to_check = '[unclear]'

    # Create a new column 'Round' to identify whether a row goes to round2 or not
    df['Round'] = df['Transcription'].apply(lambda x: 'round2' if pd.isna(x) or value_to_check in x.lower() else 'transcribe_cortex_ready')

    # Separate rows into two DataFrames based on the 'Round' column
    df_round2 = df[df['Round'] == 'round2']
    df_transcribe_cortex_ready = df[df['Round'] == 'transcribe_cortex_ready']

    # Remove the 'Round' column if you don't need it in the output CSV files
    df_round2 = df_round2.drop(columns='Round')
    df_transcribe_cortex_ready = df_transcribe_cortex_ready.drop(columns='Round')

    # Save the filtered DataFrames to their respective CSV files
    df_round2.to_csv(csv_for_round_two, index=False)
    df_transcribe_cortex_ready.to_csv(final_csv, index=False)

    print("Check complete.")


main()
