import os
import shutil
import re
from mutagen.id3 import ID3, TIT2, TPE1
import audio_module
import argparse
import json
import logging

# Configure logging
logging.basicConfig(filename='audio_processing.log', level=logging.INFO,
                    format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


# Function to remove terms from a filename
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


# Function to clean and rename the files
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
                    # Check if the filename matches the artist - title.mp3 pattern
                    if not silent:
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and process audio files")
    parser.add_argument("folder_path", help="Destination folder path to save files")
    parser.add_argument("-S", "--silent", action="store_true", help="Silent mode, no user prompts")
    args = parser.parse_args()

    if not os.path.exists(args.folder_path):
        try:
            os.makedirs(args.folder_path)
            logging.warning(f"Error: Folder does not exist. Creating!")
        except Exception as e:
            logging.error(f"Error creating folder: {e}")

    # Load terms to remove from JSON file
    terms_file = "terms.json"
    terms_to_remove = load_terms_from_json(terms_file)

    # Download and process files
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
                        shutil.move(source_file, destination_file)
                        logging.info(f"Moved {file_name} to {args.folder_path}")
                    except Exception as e:
                        logging.error(f"Error moving {file_name}: {e}")

        except Exception as e:
            logging.error(f"Error processing files in the source folder: {e}")

    except Exception as e:
        logging.error(f"Error processing input file: {e}")

    print("All operations have been completed. \nLog location: audio_processing.log")
