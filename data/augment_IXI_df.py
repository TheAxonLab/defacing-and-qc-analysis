import pandas as pd
import json

# Load the dataframe from the CSV file
df = pd.read_csv('IXI_ratings_df.tsv', sep='\t')

# Load the pairing JSON into a dictionary
with open('../randomization/IXI_blind_dict.json') as f:
    blind_dict = json.load(f)

# Rename the 'subject' column of the dataframe to 'randomized_id'
df = df.rename(columns={'subject': 'randomized_id'})

# In case the same rater gave two different ratings to the same image, we consider only the last rating and sum the time it took to rate the images
df = df.groupby(['randomized_id', 'rater_id']).agg({'dataset': 'last', 'rating': 'last', 'time_sec': 'sum', 'artifacts': 'last', 'confidence': 'last', 'comments': 'last'}).reset_index()

# Function to get value from dictionary
def get_value(key):
    # Extract only the number and remove preceding zeros
    key = key.split('-')[1].split('_')[0].lstrip('0')
    return blind_dict.get(str(int(key)), None)

# Create new column 'defacing_raw'
df['defacing_raw'] = df['randomized_id'].apply(get_value)

# Function to encode defacing
def encode_defacing(value):
    if value is None:
        return None
    parts = value.split('_')
    if 'non' in parts[1]:
        return 0
    if 'defaced' in parts[1]:
        return 1
    return None

# Create new column 'defacing'
df['defaced'] = df['defacing_raw'].apply(encode_defacing)

# Function to extract subject_id
def extract_subject_id(value):
    if value is None:
        return None
    return value.split('_')[0]

# Create new column 'subject_id'
df['subject'] = df['defacing_raw'].apply(extract_subject_id)

# Anonymize raters name
def anonymize_rater(value):
    if value is None:
        return None
    return value.replace('elda', 'rater_01').replace('emeline', 'rater_02').replace('thomas', 'rater_03').replace('jaime', 'rater_04')

df['rater_id'] = df['rater_id'].apply(anonymize_rater)

# Drop the 'defacing_raw' column as it's no longer needed
df = df.drop(columns=['defacing_raw'])

# Save the dataframe to a new CSV file
df.to_csv('IXI_augmented_ratings_df.tsv', sep='\t', index=False)
