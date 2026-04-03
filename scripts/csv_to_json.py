import pandas as pd
import json
import numpy as np

def parse_list_field(value):
    """Parse fields that contain comma-separated values into lists."""
    if pd.isna(value) or value == '':
        return []
    # Split by semicolon and strip whitespace
    return [item.strip() for item in str(value).split(';') if item.strip()]

def safe_str(value):
    """Convert value to string, handling NaN and empty values."""
    if pd.isna(value) or value == '':
        return ''
    return str(value)

def safe_float(value):
    """Convert value to float, handling NaN."""
    if pd.isna(value):
        return None
    try:
        return float(value)
    except:
        return None

def safe_bool(value):
    """Convert value to boolean."""
    if pd.isna(value) or value == '':
        return False
    if isinstance(value, bool):
        return value
    return str(value).lower() in ['true', '1', 'yes']

# Read Excel file
excel_file = pd.ExcelFile('/home/henk/DATABLE/1_Projecten/2026_Brugge_leerlingmeester2/Brugse_kunstenaars_in_het_buitenland_v4.xlsx')
agents_df = pd.read_excel(excel_file, sheet_name='People')
events_df = pd.read_excel(excel_file, sheet_name='Travels')
relations_df = pd.read_excel(excel_file, sheet_name='Relations')
locations_df = pd.read_excel(excel_file, sheet_name='Places')

# Transform agents data
peopleData = []
for _, row in agents_df.iterrows():
    artist = {
        'id': safe_str(row.get('Person_ID', '')),
        'level': safe_str(row.get('Level', '')),
        'name': safe_str(row.get('Name', '')),
        'last_name': safe_str(row.get('Last_name', '')),
        'first_name': safe_str(row.get('First_name', '')),
        'variants': parse_list_field(row.get('Name_variants', '')),
        'birth': safe_str(row.get('Date_of_birth', '')),
        'data_of_birth_prec': safe_str(row.get('Date_of_birth_precision', '')),
        'place_birth': safe_str(row.get('Place_of_birth', '')),
        'death': safe_str(row.get('Date_of_death', '')),
        'date_of_death_prec': safe_str(row.get('Date_of_death_precision', '')),
        'place_death': safe_str(row.get('Place_of_death', '')),
        'profession': parse_list_field(row.get('Profession', '')),
        'biographical_note': safe_str(row.get('Biographical_note', '')),
        'RKDartist_id': safe_str(row.get('RKD_Artist_ID', '')),
        'dynasty_or_house': safe_str(row.get('Dynasty_or_house', '')),
        'gender': safe_str(row.get('Gender', '')),
        'nationality': safe_str(row.get('Nationality', '')),
        'internal_note': safe_str(row.get('Remarks', ''))
    }
    peopleData.append(artist)

# Transform events data
travelsData = []
for _, row in events_df.iterrows():
    event = {
        'event_id': safe_str(row.get('Travel_ID', '')),
        'artist_id': safe_str(row.get('Person_ID_(traveller)', '')),
        'location': safe_str(row.get('Main_travel_destination', '')),
        'secondary_locations': parse_list_field(row.get('Secondary_places', '')),
        'description': safe_str(row.get('Travel_remark', '')),
        'start': safe_str(row.get('Arrival_date', '')),
        'start_date_prec': safe_str(row.get('Arrival_date_precision', '')),
        'start_date_source': safe_str(row.get('Arrival_date_source', '')),
        'confirmed_date': parse_list_field(row.get('Confirmed_presence', '')),
        'confirmed_date_source': safe_str(row.get('Confirmed_presence_source', '')),
        'end': safe_str(row.get('End_date', '')),
        'end_date_prec': safe_str(row.get('End_date_precision', '')),
        'end_date_source': safe_str(row.get('End_date_source', '')),
        'artwork_id': parse_list_field(row.get('Artwork_id', '')),
        'event_note': safe_str(row.get('Event_note', '')),
        'financial_means_of_travel': safe_str(row.get('Financial_means_of_travel', ''))
    }
    travelsData.append(event)

# Transform relations data
relations = []
for _, row in relations_df.iterrows():
    relation = {
        'relation_id': safe_str(row.get('Relation_ID', '')),
        'source': safe_str(row.get('Artist_ID', '')),
        'target': safe_str(row.get('Associated_person_ID', '')),
        'target_name': safe_str(row.get('Associated_person_full_name', '')),
        'type': parse_list_field(row.get('Role_of_associated_person', '')),
        'linked_institution': parse_list_field(row.get('Linked_institution', '')),
        'relation_source': safe_str(row.get('Relation_source', ''))
    }
    relations.append(relation)

# Transform locations data
locations = []
for _, row in locations_df.iterrows():
    location = {
        'location_id': safe_str(row.get('Place_ID', '')),
        'location_name': safe_str(row.get('Place_name', '')),
        'lat': safe_float(row.get('Latitude')),
        'lon': safe_float(row.get('Longitude'))
    }
    locations.append(location)

# Create final JSON structure
output_data = {
    'peopleData': peopleData,
    'travelsData': travelsData,
    'relations': relations,
    'Locations': locations
}

# Write to JSON file
with open('leerling_meester_sourcedata.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=3, ensure_ascii=False)

print("JSON file created successfully: leerling_meester_sourcedata.json")
print(f"Total artists: {len(peopleData)}")
print(f"Total events: {len(travelsData)}")
print(f"Total relations: {len(relations)}")
print(f"Total locations: {len(locations)}")


# Write to JS file as const variables
with open('leerling_meester_sourcedata.js', 'w', encoding='utf-8') as f:
    f.write('const peopleData = ')
    f.write(json.dumps(peopleData, indent=4, ensure_ascii=False))
    f.write(';\n\n')

    f.write('const travelsData = ')
    f.write(json.dumps(travelsData, indent=4, ensure_ascii=False))
    f.write(';\n\n')

    f.write('const relationsData = ')
    f.write(json.dumps(relations, indent=4, ensure_ascii=False))
    f.write(';\n\n')

    f.write('const Locations = ')
    f.write(json.dumps(locations, indent=4, ensure_ascii=False))
    f.write(';\n')

print("JS file created successfully: leerling_meester_sourcedata.js")
print(f"Total artists: {len(peopleData)}")
print(f"Total events: {len(travelsData)}")
print(f"Total relations: {len(relations)}")
print(f"Total locations: {len(locations)}")