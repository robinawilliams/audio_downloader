import os
import shutil

# Define the source folder (current folder) and destination folder
source_folder = os.getcwd()  # Current folder
# Prompt for filepath
folder_path = input("Please enter a folder to move files to: ")
# Ensure the destination folder exists; create it if not
if not os.path.exists(folder_path):
    print("This folder does not exist. Quitting.")
    quit()

# Ensure the destination folder exists; create it if not
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

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
