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

df = df.drop(['State', 'Country', 'City', 'Subject 1', 'Subject 2', 'Subject 3', 'Postmark Date', 'retired', 'Body of water', 'Unidentified'], axis=1)

# Create a list to store the duplicated and modified rows
#new_rows = []

# Iterate through each row in the original DataFrame
"""for _, row in df.iterrows():
    # Check if FILENAME and FILENAME2 have values
    if not pd.isna(row['FILENAME']) and not pd.isna(row['FILENAME2']):
        # Create two new rows with 'Original file name' set to FILENAME and FILENAME2
        new_row1 = row.copy()
        new_row2 = row.copy()
        
        new_row1['Original file name'] = row['FILENAME']
        new_row2['Original file name'] = row['FILENAME2']
        
        # Append the new rows to the list
        new_rows.extend([new_row1, new_row2])
    
    # Check if FILENAME1 and FILENAME2 have values
    elif not pd.isna(row['FILENAME1']) and not pd.isna(row['FILENAME2']):
        # Create two new rows with 'Original file name' set to FILENAME1 and FILENAME2
        new_row1 = row.copy()
        new_row2 = row.copy()
        
        new_row1['Original file name'] = row['FILENAME1']
        new_row2['Original file name'] = row['FILENAME2']
        
        # Append the new rows to the list
        new_rows.extend([new_row1, new_row2])
    else:
        # If neither condition is met, just append the original row
        new_rows.append(row)

# Create a new DataFrame from the list of new rows
# df = pd.DataFrame(new_rows) """

#df['Original file name'] = df['Original file name'].str.replace('_o3.jpg', '.tif')
df['Subjects'] = df['Category']

# Drop the extra columns
df = df.drop(['Category'], axis=1)

# Save the modified DataFrame to a new CSV file
df.to_csv(output_csv_file, index=False)
#new_df.to_csv(output_csv_file, index=False)

print("CSV transformation complete. Saved as:", output_csv_file)