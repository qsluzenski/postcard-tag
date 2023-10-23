import pandas as pd

# Define the file paths
input_csv_file = 'transcribe_merged.csv'  # Replace with your input CSV file path
output_csv_file = 'check.csv'  # Replace with your desired output CSV file path

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(input_csv_file)

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
df.to_csv(output_csv_file, index=False)

print("CSV transformation complete. Saved as:", output_csv_file)

df = pd.read_csv('check.csv')

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

# Define the file paths for the two CSV files
csv_file_path_round2 = 'round2.csv'
csv_file_path_transcribe_cortex_ready = 'transcribe_cortex_ready.csv'

# Save the filtered DataFrames to their respective CSV files
df_round2.to_csv(csv_file_path_round2, index=False)
df_transcribe_cortex_ready.to_csv(csv_file_path_transcribe_cortex_ready, index=False)

print("Check complete.")
