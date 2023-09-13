import pandas as pd

# Define the file paths
input_csv_file = 'classify_merged.csv'  # Replace with your input CSV file path
output_csv_file = 'classify_cortex_ready.csv'  # Replace with your desired output CSV file path

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(input_csv_file)

# Define the replacement dictionary for phrases
replacement_dict = {
    "ADVERTISEMENTS": "Advertisements",
    "AGRICULTURE": "Agriculture",
    "ALCOHOL": "Alcohol",
    "ANIMALS": "Animals",
    "BUILDINGS": "Buildings",
    "ENTERTAINERS": "Entertainers",
    "HOLIDAYS": "Holidays",
    "HUMOR": "Humor",
    "MILITARY": "Military",
    "NATURE": "Nature",
    "PEOPLE": "People",
    "POLITICSANDGOVERNMENT": "Politics and government",
    #"POSTCARDSABOUTPOSTCARDS": 
    "RELIGION": "Religion",
    "SPORTS": "Sports",
    "STREETVIEWS": "Streets",
    "TOBACCO": "Tobacco",
    "TRANSPORTATION": "Transportation",
    "RACISTSTEREOTYPES": "Ethnic stereotypes",
}

# Define the column where you want to perform replacements
column_name = 'T6'  # Replace with the actual column name

# Iterate through all rows and perform replacements
for index, row in df.iterrows():
    for old_phrase, new_phrase in replacement_dict.items():
        row[column_name] = row[column_name].replace(old_phrase, new_phrase)

# Save the modified DataFrame to a new CSV file
df.to_csv(output_csv_file, index=False)

print("CSV transformation complete. Saved as:", output_csv_file)