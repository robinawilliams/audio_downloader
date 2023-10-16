import os
import shutil
import re
from mutagen.id3 import ID3, TIT2, TPE1
import audio_module
import argparse

# Constants
TERMS_TO_REMOVE = ['(Lyrics)', '(Official Audio)', '(Original Audio)', '(Explicit)', '(EXPLICIT)', '(Audio)',
                   '(Official Lyric Video)', '(original mix)']


# Function to remove terms from a filename
def remove_terms(filename, terms):
    for term in terms:
        filename = filename.replace(' ' + term, "")
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
                if not args.silent:
                    new_name = input(
                        f"Please enter a filename that matches the expected format (artist - title) for '{filename}': ")
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
                    print(f"Skipping {filename}: Filename does not match the expected format (artist - title)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and process audio files")
    parser.add_argument("folder_path", help="Destination folder path to save files")
    parser.add_argument("-S", "--silent", action="store_true", help="Silent mode, no user prompts")
    args = parser.parse_args()

    if not os.path.exists(args.folder_path):
        os.makedirs(args.folder_path)

    # Download and process files
    input_file = "input.txt"

    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            audio_module.download_audio(line)

    print("Processing complete.")

    # Move .mp3 files
    source_folder = os.getcwd()
    files = os.listdir(source_folder)
    for file in files:
        if file.endswith(".mp3"):
            source_file = os.path.join(source_folder, file)
            destination_file = os.path.join(args.folder_path, file)
            shutil.move(source_file, destination_file)
            print(f"Moved {file} to {args.folder_path}")

    print("All .mp3 files have been moved.")

    # Clean and rename files
    clean_and_rename_files(args.folder_path, TERMS_TO_REMOVE)

    # Set MP3 tags
    set_mp3_tags(args.folder_path)
