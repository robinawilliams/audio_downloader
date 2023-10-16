import os
import re
import json

# Directory containing the files you want to rename
folder_path = input("Enter your the file path with mp3 files to rename: ")


def remove_terms(filename, terms):
    for term in terms:
        filename = filename.replace(' ' + term, "")
    return filename.strip()


# Function to load terms to remove from a JSON file
def load_terms_from_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        return data.get('terms', [])


# Function to clean and rename the files
def clean_and_rename_files(folder_path, terms_to_remove):
    pattern = r' \[(.*?)\]'
    for file in os.listdir(folder_path):
        old_name = os.path.join(folder_path, file)
        if os.path.isfile(old_name) and file.lower().endswith(".mp3"):
            new_name = re.sub(pattern, '', file)
            new_name = remove_terms(new_name, terms_to_remove)
            new_name = re.sub(r'  ', ' ', new_name)
            base, ext = os.path.splitext(new_name)
            new_name = base + os.path.splitext(file)[1]
            new_name = os.path.join(folder_path, new_name)
            os.rename(old_name, new_name)
            print(f'Renamed: {old_name} to {new_name}')


# Load terms to remove from JSON file
terms_file = "../terms.json"
terms_to_remove = load_terms_from_json(terms_file)

clean_and_rename_files(folder_path, terms_to_remove)
