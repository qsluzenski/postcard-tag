import csv
import json

def save_dict_to_json(data_dict, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)

def find_task_values(csv_file_path):
    # We will parse each row and push the results into this list
    output = [] 
    justJson = []
    skip_count = 0
    with open(csv_file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            try:
                if row[5] == "Transcribe Handwritten Messages":
                        if skip_count >= 3: # skip the first three, since that is data from before the final version
                            data_dict = json.loads(row[11]) # Assuming 0-based indexing, so 11 is the 12th column
                            if isinstance(data_dict, list):
                                justJson.append(data_dict)
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
    
    return output, justJson

csv_file_path = 'postcard-tag-classifications.csv'  # Replace with your CSV file path
outputList, justJson = find_task_values(csv_file_path)
# print(outputList)

json_file_path = 'transcribe_result.json'  # Replace with the desired output JSON file path
save_dict_to_json(outputList, json_file_path)

jjson_file_path = 'transcribe_just_json.json'  # Replace with the desired output JSON file path
save_dict_to_json(justJson, jjson_file_path)

print(f"Dictionary has been saved as {json_file_path}.")


