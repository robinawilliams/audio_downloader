import subprocess
import os
import shutil
import re
from mutagen.id3 import ID3, TIT2, TPE1

# Constants
TERMS_TO_REMOVE = [' (Lyrics)', ' (Official Audio)', ' (Original Audio)', ' (Explicit)', ' (EXPLICIT)', ' (Audio)',
                   ' (Official Lyric Video)', ' (original mix)']


# Function to remove terms from a filename
def remove_terms(filename, terms):
    for term in terms:
        filename = filename.replace(term, "")
    return filename.strip()


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

# Function to set MP3 tags from the filename
def set_mp3_tags(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp3"):
            file_path = os.path.join(folder_path, filename)
            try:
                base_filename = os.path.splitext(filename)[0]
                artist, title = base_filename.split(' - ', 1)
                audio = ID3(file_path)
                audio["TPE1"] = TPE1(encoding=3, text=artist)
                audio["TIT2"] = TIT2(encoding=3, text=title)
                audio.save()
                print(f"Updated tags for {filename}: Artist - {artist}, Title - {title}")
            except (ValueError, IndexError):
                print(f"Skipping {filename}: Filename does not match the expected format (artist - title)")


def main():
    folder_path = input("Please enter a filepath to download files to: ")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Download and process files
    input_file = "input.txt"
    process_script = "audio.py"

    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            command = ['python', process_script, line]
            try:
                subprocess.check_call(command)
            except subprocess.CalledProcessError:
                print(f"Error while processing: {line}")

    print("Processing complete.")

    # Move .mp3 files
    source_folder = os.getcwd()
    files = os.listdir(source_folder)
    for file in files:
        if file.endswith(".mp3"):
            source_file = os.path.join(source_folder, file)
            destination_file = os.path.join(folder_path, file)
            shutil.move(source_file, destination_file)
            print(f"Moved {file} to {folder_path}")

    print("All .mp3 files have been moved.")

    # Clean and rename files
    clean_and_rename_files(folder_path, TERMS_TO_REMOVE)

    # Set MP3 tags
    set_mp3_tags(folder_path)


if __name__ == "__main__":
    main()
