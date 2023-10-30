import csv
import json

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

def save_dict_to_json(data_dict, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(data_dict, json_file, indent=4)

def find_task_values(csv_file_path):
    # Parse each row and push the results into this list
    output = [] 
    justJson = []
    skip_count = 0
    with open(csv_file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            try:
                if row[5] == "Classify Postcards":
                        if skip_count >= 7: # skip the first seven, since that is data from before the final version
                            data_dict = json.loads(row[11]) # Assuming 0-based indexing, so 11 is the 12th column
                            if isinstance(data_dict, list):
                                justJson.append(data_dict)
                                # this is the row's output, which will be pushed into the final list
                                outpObj = {}
                                for i in data_dict:
                                # Structure of required code for each Zooniverse question type described in Postcard Tag bible
                                    if i['task'] == 'T0':
                                        for j in i["value"]:
                                            if j['task'] == 'T1' and len(j["value"]) > 0:
                                                outpObj["Title"] = j["value"]
                                            elif j['task'] == 'T2':
                                                for l in j["value"]:
                                                    if "label" in l:
                                                        outpObj["Language"] = l["label"]
                                            elif j['task'] == 'T3' and len(j["value"]) > 0:
                                                outpObj["Title"] = j["value"]
                                    if i['task'] == 'T5':
                                        for j in i["value"]:
                                            if j['task'] == 'T6':
                                                outpObj[ "Subject" ] = []
                                                for q in j["value"]:
                                                    outpObj[ "Subject" ].append(q["choice"])
                                                    try: 
                                                        question = qa_pairs[q["choice"]]
                                                        if len(q["answers"][question]) > 0:
                                                            for a in q["answers"][question]:
                                                                outpObj[ "Subject" ].append(a)
                                                    # if this choice doesnt have a question / isn't in our QA dict, move on
                                                    except KeyError: 
                                                        pass
                                            elif j['task'] == 'T7' and len( j["value"] ) > 0:
                                                outpObj["Subject 2"] = j["value"]
                                    if i['task'] == 'T8':
                                        for j in i["value"]:
                                            if j['task'] == 'T9' and len( j["value"] ) > 0:
                                                outpObj["Date"] = j["value"]
                                            elif j['task'] == 'T11' and len( j["value"] ) > 0:
                                                outpObj["Publisher"] = j["value"]
                                            elif j['task'] == 'T20' and len( j["value"] ) > 0:
                                                outpObj["Postmark date"] = j["value"]
                                    if i['task'] == 'T12':
                                        for j in i["value"]:
                                            if j['task'] == 'T14':
                                                for l in j["value"]:
                                                    if "label" in l:
                                                        outpObj["State"] = l["label"]
                                            elif j['task'] == 'T15' and len(j["value"]) > 0:
                                                outpObj["City"] = j["value"]
                                            elif j['task'] == 'T17' and len(j["value"]) > 0:
                                                outpObj["Country"] = j["value"]
                                            elif j['task'] == 'T18' and len(j["value"]) > 0:
                                                outpObj["City"] = j["value"]
                                            elif j['task'] == 'T21' and len(j["value"]) > 0:
                                                outpObj["Body of water"] = j["value"]
                                            elif j['task'] == 'T19':
                                                outpObj["Unidentified"] = j["value"]
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

json_file_path = 'classify_result.json'  # Replace with the desired output JSON file path
save_dict_to_json(outputList, json_file_path)

jjson_file_path = 'classify_just_json.json'  # Replace with the desired output JSON file path
save_dict_to_json(justJson, jjson_file_path)

print(f"Dictionary has been saved as {json_file_path}.")


