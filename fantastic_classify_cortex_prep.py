import pandas as pd
import csv

# Define the file paths
input_csv_file = 'fantastic_classify_merged.csv'  # Replace with your input CSV file path
output_csv_file = 'fantastic_classify_ready.csv'  # Replace with your desired output CSV file path

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(input_csv_file)

# Define the replacement dictionary for phrases
replacement_dict = {
    "Haley's Comet / End of the world": "Halley's Comet",
    "Oversized or imaginary animals": "Animals | Humor",
    "Oversized food": "Food | Humor",
    "Transportation / In the future": "Transportation",
    "Wavy buildings / Intoxication": "Intoxication",
    "Other": "",
}

# Define the column where you want to perform replacements
column_name = 'Category'  # Replace with the actual column name

# Iterate through all rows and perform replacements
for index, row in df.iterrows():
    for old_phrase, new_phrase in replacement_dict.items():
        row[column_name] = row[column_name].replace(old_phrase, new_phrase)

df[column_name] = df['Category'].fillna('') + ' | ' + df['Subject 1'].fillna('') + ' | ' + df['Subject 2'].fillna('') + ' | ' + df['Subject 3'].fillna('')

# Drop the extra columns
df = df.drop(['Subject 1', 'Subject 2', 'Subject 3', 'Postmark Date', 'retired', 'Body of water', 'Unidentified'], axis=1)

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

# Apply the custom function to create the "Location" column
df['Location'] = df.apply(create_location, axis=1)

# Save the modified DataFrame to a new CSV file
df.to_csv(output_csv_file, index=False)

print("CSV transformation complete. Saved as:", output_csv_file)