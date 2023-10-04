import pandas as pd
import csv

# Define the file paths
input_csv_file = 'american_classify_merged.csv'  # Replace with your input CSV file path
output_csv_file = 'american_classify_ready.csv'  # Replace with your desired output CSV file path

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(input_csv_file)

# Define the replacement dictionary for phrases
replacement_dict = {
    "Aerial views & skylines": "Aerial views",
    "Beaches & bodies of water": "Beaches | Bodies of water",
    "Boats & ships": "Boats | Ships",
    "Business & industry": "Business",
    "Cartoons & humor": "Cartoons",
    "Large letters": "Graphic design (Typography)",
    "Libraries, galleries & museums": "Libraries | Galleries & museums",
    "Parks & gardens": "Parks",
    "Politics & government": "Politics and government",
    "Restaurants & bars": "Restaurants",
    "Streets & highways": "Streets",
    "World's fairs": "World's Fair",
    "Other": "",
}

# Define the column where you want to perform replacements
column_name = 'Category'  # Replace with the actual column name
df[column_name] = df[column_name].astype(str)

# Iterate through all rows and perform replacements
for index, row in df.iterrows():
    for old_phrase, new_phrase in replacement_dict.items():
        row[column_name] = row[column_name].replace(old_phrase, new_phrase)

df[column_name] = df['Category'].fillna('') + ' | ' + df['Subject 1'].fillna('') + ' | ' + df['Subject 2'].fillna('') + ' | ' + df['Subject 3'].fillna('')

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

df['Original file name'] = df['FILENAME'].str.replace('_o3.jpg', '.tif')
df['Subjects'] = df['Category']

df = df.drop(['Category', 'State', 'Country', 'City', 'Subject 1', 'Subject 2', 'Subject 3', 'retired', 'SUBJECT', 'Body of water', 'Unidentified', 'FILENAME'], axis=1)

# Save the modified DataFrame to a new CSV file
df.to_csv(output_csv_file, index=False)
#new_df.to_csv(output_csv_file, index=False)

print("CSV transformation complete. Saved as:", output_csv_file)