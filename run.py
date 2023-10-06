import subprocess
import os
from mutagen.id3 import ID3, TIT2, TPE1
import shutil

# Prompt for filepath
folder_path = input("Please enter a filepath to download files to ")
# Ensure the destination folder exists; create it if not
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# BRUTE_FORCE.PY #######################################################

input_file = "input.txt"
process_script = "audio.py"

with open(input_file, 'r') as file:
    for line in file:
        line = line.strip()  # Remove leading/trailing whitespace and newline characters
        command = ['python', process_script, line]

        try:
            subprocess.check_call(command)
        except subprocess.CalledProcessError:
            print(f"Error while processing: {line}")

print("Processing complete.")

# FILE_MOVER.PY #######################################################

# Define the source folder (current folder) and destination folder
source_folder = os.getcwd()  # Current folder

# Get a list of all files in the source folder
files = os.listdir(source_folder)

# Loop through the files and move .mp3 files to the destination folder
for file in files:
    if file.endswith(".mp3"):
        source_file = os.path.join(source_folder, file)
        destination_file = os.path.join(folder_path, file)
        shutil.move(source_file, destination_file)
        print(f"Moved {file} to {folder_path}")

print("All .mp3 files have been moved.")

# RENAME.PY #######################################################

# List all files in the folder
file_list = os.listdir(folder_path)

# Iterate through each file and rename it
for filename in file_list:
    old_filepath = os.path.join(folder_path, filename)

    # Check if the file name contains '['
    if '[' in filename:
        # Split the file name at the first '[' character
        new_filename = filename.split('[', 1)[0].strip()

        # Create the new file path
        new_filepath = os.path.join(folder_path, new_filename)

        # Rename the file
        os.rename(old_filepath, new_filepath)
        print(f'Renamed: {filename} -> {new_filename}')
    else:
        print(f'Skipped: {filename} (no [ character)')

print('Renaming complete.')

# Append .mp3 to the filename.
# I tried other fixes. I'm being lazy.
for filename in os.listdir(folder_path):
    if filename.endswith(".mp3"):
        continue  # Skip files that already have .mp3 extension
    os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, filename + ".mp3"))

print('File extension renamed to .mp3')


# MP3TAG.PY #######################################################

# Function to set MP3 tags from the filename
def set_mp3_tags(filename):
    try:
        # Extract the filename without the extension
        base_filename = os.path.splitext(os.path.basename(filename))[0]

        # Split the filename into artist and title based on the hyphen
        artist, title = base_filename.split(' - ', 1)

        # Get the MP3 file
        audio = ID3(filename)

        # Set the artist and title tags
        audio["TPE1"] = TPE1(encoding=3, text=artist)
        audio["TIT2"] = TIT2(encoding=3, text=title)

        # Save the changes
        audio.save()

        print(f"Updated tags for {filename}: Artist - {artist}, Title - {title}")

    except (ValueError, IndexError):
        print(f"Skipping {filename}: Filename does not match the expected format (artist - title)")


# Loop through MP3 files in the directory and set tags
for filename in os.listdir(folder_path):
    if filename.endswith(".mp3"):
        file_path = os.path.join(folder_path, filename)
        set_mp3_tags(file_path)
