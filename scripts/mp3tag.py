import os
from mutagen.id3 import ID3, TIT2, TPE1

# Prompt for filepath
folder_path = input("Please enter a folder to tag: ")
# Ensure the destination folder exists; create it if not
if not os.path.exists(folder_path):
    print("This folder does not exist. Quitting.")
    quit()


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
