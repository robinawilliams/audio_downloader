import os
import shutil
import re
from mutagen.id3 import ID3, TIT2, TPE1
import audio_module  # Core logic
import argparse
import json
import hashlib
import logging

# Configure logging to record events and errors in a log file
logging.basicConfig(filename='audio_processing.log', level=logging.INFO,
                    format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


# Function to remove specified terms from a filename
def remove_terms(filename, terms):
    for term in terms:
        filename = filename.replace(f' {term}', "")
    return filename.strip()


# Function to load terms to remove from a JSON file
def load_terms_from_json(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            return data.get('terms', [])
    except Exception as e:
        logging.error(f"Error loading terms from JSON file: {e}")
        return []


# Function to clean and rename files in a given folder
def clean_and_rename_files(folder_path, terms_to_remove):
    pattern = r' \[(.*?)\]'
    try:
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path) and os.path.splitext(file_name)[1].lower() == ".mp3":
                new_name = re.sub(pattern, '', file_name)
                new_name = remove_terms(new_name, terms_to_remove)
                new_name = re.sub(r'  ', ' ', new_name)
                new_name = os.path.join(folder_path, new_name)
                try:
                    os.rename(file_path, new_name)
                    logging.info(f'Renamed: {file_name} to {new_name}')
                except Exception as e:
                    logging.error(f"Error renaming {file_name}: {e}")
    except Exception as e:
        logging.error(f"Error cleaning and renaming files: {e}")


# Function to set MP3 tags from the filename
def set_mp3_tags(folder_path, silent=False):
    try:
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
                    logging.info(f"Updated tags for {file_name}: Artist: {artist}, Title: {title}")
                except (ValueError, IndexError) as ve:
                    # Handle cases where filename doesn't match the artist - title.mp3 format
                    if not silent:
                        # User input to correct the format
                        logging.error(f"Error processing tags for {file_name}: {ve}")
                        new_name = input(
                            f"Please enter a filename that matches the "
                            f"expected format (artist - title) for '{file_name}': \n")
                        new_name = new_name.strip()

                        # Remove file extension if provided by the user
                        new_name, _ = os.path.splitext(new_name)

                        new_path = os.path.join(folder_path, new_name + ".mp3")
                        os.rename(file_path, new_path)
                        artist, title = new_name.split(' - ', 1)
                        audio = ID3(new_path)
                        audio["TPE1"] = TPE1(encoding=3, text=artist)
                        audio["TIT2"] = TIT2(encoding=3, text=title)
                        audio.save()
                        logging.info(f"Updated tags for {new_name}: Artist: {artist}, Title: {title}")
                    else:
                        logging.warning(
                            f"Skipping {file_name}: Filename does not match the expected format (artist - title)")
                except Exception as e:
                    logging.error(f"Error processing tags for {file_name}: {e}")
    except Exception as e:
        logging.error(f"Error setting MP3 tags: {e}")


# Function to calculate file hash
def filehash(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Download and process audio files")
    parser.add_argument("folder_path", help="Destination folder path to save files")
    parser.add_argument("-S", "--silent", action="store_true", help="Silent mode, no user prompts")
    args = parser.parse_args()

    # Check if the specified folder exists, create it if not
    if not os.path.exists(args.folder_path):
        try:
            os.makedirs(args.folder_path)
            logging.warning(f"Error: Folder does not exist. Creating!")
        except Exception as e:
            logging.error(f"Error creating folder: {e}")

    # Load terms to remove from JSON file
    terms_file = "terms.json"
    terms_to_remove = load_terms_from_json(terms_file)

    # Download and process files based on input file
    input_file = "input.txt"
    processed_lines = []

    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                try:
                    audio_module.download_audio(line)
                    processed_lines.append(line)
                    logging.info(f"Downloaded {line}")
                except Exception as e:
                    logging.error(f"Error downloading audio for {line}: {e}")

        # Remove processed lines from input file
        with open(input_file, 'w') as file:
            file.writelines(line + '\n' for line in lines if line.strip() not in processed_lines)
            logging.info(f"Removed from input.txt: \n{line} ")

        logging.info("Downloading complete.")

        # Clean and rename files in the source folder
        source_folder = os.getcwd()
        try:
            for file_name in os.listdir(source_folder):
                file_path = os.path.join(source_folder, file_name)
                if os.path.isfile(file_path) and os.path.splitext(file_name)[1].lower() == ".mp3":
                    try:
                        clean_and_rename_files(source_folder, terms_to_remove)
                        set_mp3_tags(source_folder, args.silent)
                    except Exception as e:
                        logging.error(f"Error processing {file_name}: {e}")

            # Move .mp3 files to the final output location
            for file_name in os.listdir(source_folder):
                if os.path.splitext(file_name)[1].lower() == ".mp3":
                    source_file = os.path.join(source_folder, file_name)
                    destination_file = os.path.join(args.folder_path, file_name)
                    try:
                        # Check if the source and destination are on the same file system
                        if os.stat(source_file).st_dev == os.stat(args.folder_path).st_dev:
                            shutil.move(source_file, destination_file)
                        else:
                            shutil.copy(source_file, destination_file)

                            # Verify that the source and destination files are the same using hash check
                            if filehash(source_file) == filehash(destination_file):
                                os.remove(source_file)
                                logging.info(f"Primary activated. Moved {file_name} to {args.folder_path}")
                            else:
                                logging.warning(f"Hash mismatch for {file_name}. Keeping both files.")

                    except Exception as e:
                        logging.error(f"Error moving {file_name}: {e}")

                        # Verify that the source and destination files are the same using hash check
                        if filehash(source_file) == filehash(destination_file):
                            os.remove(source_file)
                            logging.info(f"Fallback activated. Moved {file_name} to {args.folder_path}")
                        else:
                            logging.warning(f"Hash mismatch for {file_name}. Keeping both files.")

        except Exception as e:
            logging.error(f"Error processing files in the source folder: {e}")

    except Exception as e:
        logging.error(f"Error processing input file: {e}")

    print("All operations have been completed. \nLog location: audio_processing.log")
