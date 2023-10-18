import os
import shutil
import re
from mutagen.id3 import ID3, TIT2, TPE1
import audio_module
import argparse
import json

# Function to remove terms from a filename
def remove_terms(filename, terms):
    for term in terms:
        filename = filename.replace(f' {term}', "")
    return filename.strip()

# Function to load terms to remove from a JSON file
def load_terms_from_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        return data.get('terms', [])

# Function to clean and rename the files
def clean_and_rename_files(folder_path, terms_to_remove):
    pattern = r' \[(.*?)\]'
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and os.path.splitext(file_name)[1].lower() == ".mp3":
            new_name = re.sub(pattern, '', file_name)
            new_name = remove_terms(new_name, terms_to_remove)
            new_name = re.sub(r'  ', ' ', new_name)
            new_name = os.path.join(folder_path, new_name)
            try:
                os.rename(file_path, new_name)
                print(f'Renamed: {file_name} to {new_name}')
            except Exception as e:
                print(f"Error renaming {file_name}: {e}")

# Function to set MP3 tags from the filename
def set_mp3_tags(folder_path, silent=False):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.splitext(file_name)[1].lower() == ".mp3":
            base_filename = os.path.splitext(file_name)[0]
            try:
                artist, title = base_filename.split(' - ', 1)
                audio = ID3(file_path)
                audio["TPE1"] = TPE1(encoding=3, text=artist)
                audio["TIT2"] = TIT2(encoding=3, text=title)
                audio.save()
                print(f"Updated tags for {file_name}: Artist - {artist}, Title - {title}")
            except (ValueError, IndexError):
                if not silent:
                    new_name = input(
                        f"Please enter a filename that matches the expected format (artist - title) for '{file_name}': ")
                    new_name = new_name.strip()
                    new_name = os.path.join(folder_path, new_name + ".mp3")
                    os.rename(file_path, new_name)
                    artist, title = new_name.split(' - ', 1)
                    audio = ID3(new_name)
                    audio["TPE1"] = TPE1(encoding=3, text=artist)
                    audio["TIT2"] = TIT2(encoding=3, text=title)
                    audio.save()
                    print(f"Updated tags for {new_name}: Artist - {artist}, Title - {title}")
                else:
                    print(f"Skipping {file_name}: Filename does not match the expected format (artist - title)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and process audio files")
    parser.add_argument("folder_path", help="Destination folder path to save files")
    parser.add_argument("-S", "--silent", action="store_true", help="Silent mode, no user prompts")
    args = parser.parse_args()

    if not os.path.exists(args.folder_path):
        os.makedirs(args.folder_path)

    # Load terms to remove from JSON file
    terms_file = "terms.json"
    terms_to_remove = load_terms_from_json(terms_file)

    # Download and process files
    input_file = "input.txt"

    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            audio_module.download_audio(line)

    print("Processing complete.")

    # Clean and rename files in the source folder
    source_folder = os.getcwd()
    for file_name in os.listdir(source_folder):
        file_path = os.path.join(source_folder, file_name)
        if os.path.isfile(file_path) and os.path.splitext(file_name)[1].lower() == ".mp3":
            clean_and_rename_files(source_folder, terms_to_remove)
            set_mp3_tags(source_folder, args.silent)

    # Move .mp3 files to the final output location
    for file_name in os.listdir(source_folder):
        if os.path.splitext(file_name)[1].lower() == ".mp3":
            source_file = os.path.join(source_folder, file_name)
            destination_file = os.path.join(args.folder_path, file_name)
            try:
                shutil.move(source_file, destination_file)
                print(f"Moved {file_name} to {args.folder_path}")
            except Exception as e:
                print(f"Error moving {file_name}: {e}")

    print("All .mp3 files have been moved.")
