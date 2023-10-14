import os
import re

# Directory containing the files you want to rename
folder_path = input("Enter the filepath for the folder you want: ")

# Regular expression pattern to match everything after the first '[' and any trailing spaces
pattern = r' \[.*'

# List of terms to remove
terms_to_remove = [' (Lyrics)', ' (Official Audio)', ' (Explicit)', ' (EXPLICIT)', ' (Audio)',
                   ' (Official Lyric Video)', ' (original mix)'
                   ]


# Function to remove terms from a filename
def remove_terms(filename, terms):
    for term in terms:
        filename = filename.replace(term, "")
    return filename.strip()  # Use strip() to remove trailing spaces


# List all files in the specified folder
files = os.listdir(folder_path)

for file in files:
    old_name = os.path.join(folder_path, file)

    # Check if the file is a regular file (not a directory)
    if os.path.isfile(old_name):
        # Use a regular expression to remove everything after the first '[' and trailing spaces
        new_name = re.sub(pattern, '', file)

        # Remove the specified terms
        new_name = remove_terms(new_name, terms_to_remove)

        # Remove double spaces
        new_name = re.sub(r'  ', ' ', new_name)

        # Add the file extension back to the new name
        if file != new_name:
            base, ext = os.path.splitext(new_name)
            new_name = base + os.path.splitext(file)[1]

        new_name = os.path.join(folder_path, new_name)

        # Rename the file
        os.rename(old_name, new_name)
        print(f'Renamed: {old_name} to {new_name}')
