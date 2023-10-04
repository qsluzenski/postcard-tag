import csv
import json

def save_dict_to_json(data_dict, file_path):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data_dict, json_file, indent=4)

def find_task_values(csv_file_path):
    # We will parse each row and push the results into this list
    output = [] 
    justJson = []
    with open(csv_file_path, 'r', encoding='utf-8', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            try:
                if row[5] == "Fantastic Scenes":
                        data_dict = json.loads(row[11]) # Assuming 0-based indexing, so 11 is the 12th column
                        if isinstance(data_dict, list):
                            justJson.append(data_dict)
                            # this is the row's output, which will be pushed into the final list
                            outpObj = {}
                            for i in data_dict:
                                if i['task'] == 'T0':
                                    for j in i["value"]:
                                        if j['task'] == 'T1':
                                            for d in j["value"]:
                                                if d["tool_label"] == 'Caption/Title':
                                                    if "details" in d:
                                                        for v in d["details"]:
                                                            if "value" in v:
                                                                outpObj["Title"] = v["value"]
                                                if d["tool_label"] == 'Title/caption':
                                                    if "details" in d:
                                                        for v in d["details"]:
                                                            if "value" in v:
                                                                outpObj["Title"] = v["value"]
                                                if d["tool_label"] == 'Date (postmark - year only)':
                                                    if "details" in d:
                                                        for v in d["details"]:
                                                            if "value" in v:
                                                                outpObj["Postmark Date"] = v["value"]
                                                if d["tool_label"] == 'Date (publication or copyright)':
                                                    if "details" in d:
                                                        for v in d["details"]:
                                                            if "value" in v:
                                                                outpObj["Date"] = v["value"]
                                                if d["tool_label"] == 'Publisher':
                                                    if "details" in d:
                                                        for v in d["details"]:
                                                            if "value" in v:
                                                                outpObj["Publisher"] = v["value"]
                                        elif j['task'] == 'T2' and len(j["value"]) > 0:
                                            outpObj["Title"] = j["value"]
                                if i['task'] == 'T27':
                                    for d in i["value"]:
                                        if d["tool_label"] == 'Date -- postmark':
                                            if "details" in d:
                                                for v in d["details"]:
                                                    if "value" in v:
                                                        outpObj["Postmark Date"] = v["value"]
                                        if d["tool_label"] == 'Date -- publication or copyright':
                                            if "details" in d:
                                                for v in d["details"]:
                                                    if "value" in v:
                                                        outpObj["Date"] = v["value"]
                                        if d["tool_label"] == 'Publisher':
                                            if "details" in d:
                                                for v in d["details"]:
                                                    if "value" in v:
                                                        outpObj["Publisher"] = v["value"]
                                if i['task'] == 'T25':
                                    for j in i["value"]:
                                        if j['task'] == 'T21':
                                            for l in j["value"]:
                                                if "label" in l and l["select_label"] == 'select state:':
                                                    outpObj["State"] = l["label"]
                                                elif "label" in l and l["select_label"] == 'Country':
                                                    outpObj["Country"] = l["label"]
                                        elif j['task'] == 'T26' and len( j["value"] ) > 0 and j["task_label"] == "Enter U.S. city name:":
                                            outpObj["City"] = j["value"]
                                        elif j['task'] == 'T26' and len( j["value"] ) > 0 and j["task_label"] == "If you selected \"Other\" from the drop-down menu, enter the country name here:":
                                            outpObj["Country"] = j["value"]
                                        elif j['task'] == 'T23':
                                            for l in j["value"]:
                                                    if "label" in l:
                                                        outpObj["State"] = l["label"]
                                                    elif len( j["value"] ) > 0 and "select_label" not in l:
                                                        outpObj["Body of water"] = j["value"]
                                        elif j['task'] == 'T24' and len( j["value"] ) > 0 and j["task_label"] == "For **non-U.S. locations**, enter country name:":
                                            outpObj["Country"] = j["value"]
                                        elif j['task'] == 'T24' and len( j["value"] ) > 0 and j["task_label"] == "**For all locations,** enter name of city:":
                                            outpObj["City"] = j["value"]
                                        elif j['task'] == 'T28' and len( j["value"] ) > 0:
                                            outpObj["City"] = j["value"]
                                        elif j['task'] == 'T22' and j["value"] != None:
                                            outpObj["Unidentified"] = j["value"]
                                if i['task'] == 'T13':
                                    for j in i["value"]:
                                        if j['task'] == 'T14':
                                            for l in j["value"]:
                                                if "label" in l:
                                                    outpObj["Category"] = l["label"]
                                        elif j['task'] == 'T16' and len( j["value"] ) > 0:
                                            outpObj["Subject 2"] = j["value"]
                                        elif j['task'] == 'T17' and len( j["value"] ) > 0:
                                            outpObj["Subject 3"] = j["value"]
                                        elif j['task'] == 'T18' and len( j["value"] ) > 0:
                                            outpObj["Subject 1"] = j["value"]
                                if i['task'] == 'T19':
                                    for j in i["value"]:
                                        if j['task'] == 'T20' and len(j["value"]) > 0:
                                            outpObj["Other information"] = j["value"]
                            output.append(outpObj)
            except json.JSONDecodeError:
                print('json parse FAIL')
                # Move on if JSON parsing fails
                pass
    
    return output, justJson

csv_file_path = 'postcard-tag-old-classifications.csv'  # Replace with your CSV file path
outputList, justJson = find_task_values(csv_file_path)
# print(outputList)

json_file_path = 'fantastic_classify_result.json'  # Replace with the desired output JSON file path
save_dict_to_json(outputList, json_file_path)

jjson_file_path = 'fantastic_classify_just_json.json'  # Replace with the desired output JSON file path
save_dict_to_json(justJson, jjson_file_path)

print(f"Dictionary has been saved as {json_file_path}.")


