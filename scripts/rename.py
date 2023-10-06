import os

# Prompt for filepath
folder_path = input("Please enter a filepath: ")
# Ensure the destination folder exists; create it if not
if not os.path.exists(folder_path):
    print("This folder does not exist. Quitting.")
    quit()

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
