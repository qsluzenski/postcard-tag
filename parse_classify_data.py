import csv
import json
import pandas as pd

# Identify the subject/question pairs for the subjects with question options
qa_pairs = {
    "HUMOR": "ISTHECARDACARTOON",
    "ANIMALS": "WHATKINDOFANIMAL",
    "HOLIDAYS": "WHICHHOLIDAY",
    "NATURE": "WHATKINDOFNATURESCENE",
    "RELIGION": "WHATKINDOFRELIGIOUSSCENE",
    "PEOPLE": "WHATCANYOUIDENTIFYABOUTTHESEPEOPLE",
    "POLITICSANDGOVERNMENT": "WHATKINDOFPOLITICALIMAGE",
    "SPORTS": "WHICHSPORT",
    "TRANSPORTATION": "WHATKINDOFTRANSPORTATION",
    "BUILDINGS": "WHATKINDOFBUILDING",
    "STREETVIEWS": "WHATKINDOFSTREETVIEW",
}

input_csv = 'postcard-tag-classifications.csv'
data_output_json = 'classify_result.json'
raw_json = 'classify_just_json.json'
file_name_json = "classify_file_name.json"
merged_output_json = "classify_merged_output.json"
merged_csv = "classify_merged.csv"
output_csv_file = 'classify_cortex_ready.csv'


def main():
    data_output, raw_data = find_task_values(input_csv)
    save_dict_to_json(data_output, data_output_json)
    save_dict_to_json(raw_data, raw_json)
    get_file_names(input_csv, file_name_json)
    merge_data_and_file_names(file_name_json, data_output_json)
    cortex_prep(merged_csv)


def find_task_values(raw_csv):
    # Parse each row and push the results into this list
    output = []
    just_json = []
    skip_count = 0
    with open(raw_csv, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            try:
                if row[5] == "Classify Postcards":
                    if skip_count >= 7:  # skip the first seven, since that is data from before the final version
                        data_dict = json.loads(row[11])  # Assuming 0-based indexing, so 11 is the 12th column
                        if isinstance(data_dict, list):
                            just_json.append(data_dict)
                            # this is the row's output, which will be pushed into the final list
                            output_data = {}
                            for i in data_dict:
                                if i['task'] == 'T0':  # task category code for first page
                                    for j in i["value"]:
                                        if j['task'] == 'T1' and len(j["value"]) > 0:  # task: caption text on postcard
                                            output_data["Title"] = j["value"]  # output to Title field
                                        elif j['task'] == 'T2':  # task: language of postcard
                                            for label in j["value"]:  # dropdown menu task, so needs more nested code
                                                if "label" in label:
                                                    output_data["Language"] = label["label"]  # output to Language field
                                        elif j['task'] == 'T3' and len(j["value"]) > 0:  # task: user-written caption
                                            output_data["Title"] = j["value"]  # output to Title field
                                if i['task'] == 'T5':  # task category code for subject page
                                    for j in i["value"]:
                                        if j['task'] == 'T6':  # task: subject; survey task. requires QA dict
                                            output_data["Subject"] = []
                                            for q in j["value"]:
                                                output_data["Subject"].append(q["choice"])
                                                try:
                                                    question = qa_pairs[q["choice"]]
                                                    if len(q["answers"][question]) > 0:
                                                        for a in q["answers"][question]:
                                                            output_data["Subject"].append(a)  # output to Subject field
                                                # if this choice doesn't have a question / isn't in our QA dict, move on
                                                except KeyError:
                                                    pass
                                        elif j['task'] == 'T7' and len(j["value"]) > 0:  # task: user-written subject
                                            output_data["User subject"] = j["value"]  # output to alt Subject field
                                if i['task'] == 'T8':  # task category code for details page
                                    for j in i["value"]:
                                        if j['task'] == 'T9' and len(j["value"]) > 0:  # task: date
                                            output_data["Date"] = j["value"]
                                        elif j['task'] == 'T11' and len(j["value"]) > 0:  # task: date
                                            output_data["Publisher"] = j["value"]
                                        elif j['task'] == 'T20' and len(j["value"]) > 0:  # task: date
                                            output_data["Postmark date"] = j["value"]
                                if i['task'] == 'T12':  # task category code for location page
                                    for j in i["value"]:
                                        if j['task'] == 'T14':  # task: state (dropdown menu)
                                            for label in j["value"]:
                                                if "label" in label:
                                                    output_data["State"] = label["label"]
                                        elif j['task'] == 'T15' and len(j["value"]) > 0:  # task: US city
                                            output_data["City"] = j["value"]
                                        elif j['task'] == 'T17' and len(j["value"]) > 0:  # task: country
                                            output_data["Country"] = j["value"]
                                        elif j['task'] == 'T18' and len(j["value"]) > 0:  # task: non-US city
                                            output_data["City"] = j["value"]
                                        elif j['task'] == 'T21' and len(j["value"]) > 0:  # task: body of water
                                            output_data["Body of water"] = j["value"]
                                        elif j['task'] == 'T19':  # task: if "unidentified" is selected
                                            output_data["Unidentified"] = j["value"]
                            output.append(output_data)
                    else:
                        skip_count += 1
            except json.JSONDecodeError:
                print('json parse FAIL')
                # Move on if JSON parsing fails
                pass

    return output, just_json


def save_dict_to_json(data_dict, file_path):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data_dict, json_file, indent=4)
    print(f"Dictionary has been saved as {data_output_json}.")


def get_file_names(raw_csv, file_name_json_file):
    output_list = []
    skip_count = 0

    # Read the CSV file and pull out the file name information
    with open(raw_csv, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            try:
                if row[5] == "Classify Postcards":
                    if skip_count >= 7:
                        json_data = json.loads(row[12])
                        if isinstance(json_data, dict):  # check if it's a dictionary
                            for value in json_data.values():
                                output_list.append(value)  # add each value to the list
                        else:
                            print("JSON data in row is not in expected format:", json_data)
                    else:
                        skip_count += 1
            except json.JSONDecodeError:
                print(f"Error parsing JSON in row: {row}")

    with open(file_name_json_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(output_list, jsonfile, indent=4)


def merge_data_and_file_names(file_name_json_file, data_output_json_file):
    # Load content from JSON files
    with open(file_name_json_file, 'r', encoding='utf-8') as file1, open(data_output_json_file, "r") as file2:
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
    with open(merged_output_json, 'w', encoding='utf-8') as output_file:
        json.dump(merged_data, output_file, indent=4)

    print("Merged data written to", merged_output_json)

    # Load content from JSON file
    with open(merged_output_json, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Headers from the two JSON files for the new CSV
    header = ["retired", "Original file name", "Original file name_1", "#Unique identifier", "#Unique identifier_1",
              "#Unique identifier backs", "#Unique identifier fronts", "Title", "Language", "Date", "Postmark date",
              "Publisher", "City", "State", "Country", "Body of water", "Subject", "User subject", "Unidentified"]

    # Write JSON data to CSV
    with open(merged_csv, 'w', newline="", encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=header)

        # Write the header row
        csv_writer.writeheader()

        # Write each dictionary as a row in the CSV file
        for entry in data:
            if entry["retired"] is not None:  # Only write if "retired" is not null
                csv_writer.writerow(entry)

    print("JSON data converted to CSV:", merged_csv)


def cortex_prep(csv_merged):

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_merged)

    # Define the replacement dictionary for phrases in the data to replace with subject headings
    replacement_dict = {
        "'ADVERTISEMENTS'": "Advertisements",
        "'AGRICULTURE'": "Agriculture",
        "'ALCOHOL'": "Alcohol",
        "'ANIMALS'": "Animals",
        "'BUILDINGS'": "Buildings",
        "'ENTERTAINERS'": "Entertainers",
        "'HOLIDAYS'": "Holidays",
        "'HUMOR'": "Humor",
        "'MILITARY'": "Military",
        "'NATURE'": "Nature",
        "'PEOPLE'": "People",
        "'POLITICSANDGOVERNMENT'": "Politics and government",
        "'POSTCARDSABOUTPOSTCARDS'": "Postcard history",
        "'RELIGION'": "Religion",
        "'SPORTS'": "Sports",
        "'STREETVIEWS'": "Streets",
        "'TOBACCO'": "Tobacco",
        "'TRANSPORTATION'": "Transportation",
        "'RACISTSTEREOTYPES'": "Ethnic stereotypes",
        "'CARICATURESANDCARTOONS'": "Caricatures",
        "'DOGS'": "Dogs",
        "'CATS'": "Cats",
        "'HORSES'": "Horses",
        "'BIRDS'": "Birds",
        "'CHRISTMAS'": "Christmas",
        "'EASTER'": "Easter",
        "'SAINTPATRICKSDAY'": "Saint Patrick’s Day",
        "'THANKSGIVING'": "Thanksgiving",
        "'HALLOWEEN'": "Halloween",
        "'BIRTHDAYS'": "Birthdays",
        "'NEWYEAR'": "New Year",
        "'VALENTINESDAY'": "Valentine’s Day",
        "'FOURTHOFJULY'": "Fourth of July",
        "'SANTACLAUS'": "Santa Claus",
        "'MOUNTAINS'": "Mountains",
        "'FLOWERS'": "Flowers",
        "'RIVERS'": "Rivers",
        "'LAKES'": "Lakes",
        "'WATERFALLS'": "Waterfalls",
        "'CHRISTIANITY'": "Christianity",
        "'BAPTISM'": "Baptism",
        "'JUDAISM'": "Judaism",
        "'HINDUISM'": "Hinduism",
        "'BUDDHISM'": "Buddhism",
        "'ISLAM'": "Islam",
        "'AFRICANAMERICANS'": "African Americans",
        "'NATIVEAMERICANS'": "Indians of North America",
        "'ASIANAMERICANS'": "Asian Americans",
        "'WOMEN'": "Women",
        "'CHILDREN'": "Children",
        "'BABIES'": "Children",
        "'CROWDS'": "Crowds",
        "'PORTRAITPHOTOGRAPHY'": "Portrait photography",
        "'PORTRAITPAINTING'": "Portrait painting",
        "'SUFFRAGE'": "Suffrage",
        "'TEMPERANCE'": "Temperance",
        "'PRESIDENTS'": "Presidents",
        "'PATRIOTISM'": "Patriotism",
        "'BASEBALL'": "Baseball",
        "'BOXING'": "Boxing",
        "'BOWLING'": "Bowling",
        "'BICYCLESTRICYCLES'": "Bicycles & tricycles",
        "'DANCE'": "Dance",
        "'FOOTBALL'": "Football",
        "'HUNTING'": "Hunting",
        "'TENNIS'": "Tennis",
        "'AIRPLANES'": "Airplanes",
        "'AUTOMOBILES'": "Automobiles",
        "'BOATS'": "Boats",
        "'CARRIAGESANDCARTS'": "Carriages and carts",
        "'RAILROADS'": "Railroads",
        "'BANKS'": "Banks",
        "'HOSPITALS'": "Hospitals",
        "'HOTELS'": "Hotels",
        "'PUBLICBUILDINGS'": "Public buildings",
        "'MONUMENTS'": "Monuments",
        "'RESIDENCES'": "Residences",
        "'SCHOOLS'": "Schools",
        "'STORESSHOPS'": "Stores & shops",
        "'BUSINESSDISTRICTS'": "Business districts",
        "'AERIALVIEWS'": "Aerial views",
        "'STREETS'": "Streets",
        "'OTHER'": "",
        "[": "",
        "]": "",
        ", ": " | ",
    }

    column_name = 'Subject'

    # Iterate through all rows and perform replacements
    for index, row in df.iterrows():
        for old_phrase, new_phrase in replacement_dict.items():
            row[column_name] = row[column_name].replace(old_phrase, new_phrase)

    # Apply the custom function to create the "Location" column
    df['Location'] = df.apply(create_location, axis=1)

    # Remove unnecessary columns
    df = df.drop(['State', 'Country', 'City', 'retired', 'Body of water', 'Unidentified',
                  '#Unique identifier', '#Unique identifier_1', '#Unique identifier backs',
                  '#Unique identifier fronts'], axis=1)

    # Duplicate each row so that there is one row for the front and one row for the back
    new_rows = []

    for _, row in df.iterrows():
        new_row1 = row.copy()
        new_row2 = row.copy()

        new_row1['Original file name'] = row['Original file name']
        new_row2['Original file name'] = row['Original file name_1']

        # Append the new rows to the list
        new_rows.extend([new_row1, new_row2])

    # Create a new DataFrame from the list of new rows
    df = pd.DataFrame(new_rows)

    df['Original file name'] = df['Original file name'].str.replace('_o3.jpg', '.tif')

    # Drop the extra file name column
    df = df.drop(['Original file name_1'], axis=1)

    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_csv_file, index=False)

    print("CSV transformation complete. Saved as:", output_csv_file)

# Convert the location input into one location column


def create_location(row):
    if row['Country'] != 'United States' and pd.isna(row['State']) and pd.notna(row['City']):
        return f"{row['Country']}--{row['City']}"
    elif row['Country'] != 'United States' and pd.isna(row['State']) and pd.isna(row['City']):
        return row['Country']
    elif pd.notna(row['State']) and pd.isna(row['City']):
        return row['State']
    elif pd.notna(row['State']) and pd.notna(row['City']):
        return f"{row['State']}--{row['City']}"
    else:
        return None  # Handle other cases if needed


if __name__ == '__main__':
    main()
