import pandas as pd

# Define the file paths
input_csv_file = 'classify_merged.csv'  # Replace with your input CSV file path
output_csv_file = 'classify_cortex_ready.csv'  # Replace with your desired output CSV file path

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(input_csv_file)

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

# Define the column where you want to perform replacements
column_name = 'Subject'

# Iterate through all rows and perform replacements
for index, row in df.iterrows():
    for old_phrase, new_phrase in replacement_dict.items():
        row[column_name] = row[column_name].replace(old_phrase, new_phrase)

# Combine the subject columns into one subject heading column
df[column_name] = df['Subject'].fillna('') + ' | ' + df['Subject 2'].fillna('')

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

# Apply the custom function to create the "Location" column
df['Location'] = df.apply(create_location, axis=1)

# Remove unnecessary columns
df = df.drop(['State', 'Country', 'City', 'Subject 2', 'retired', 'Body of water', 'Unidentified', '#Unique identifier', '#Unique identifier_1', '#Unique identifier backs', '#Unique identifier fronts'], axis=1)

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