# audio_downloader

## A python tool to automatically download the audio of a video and set its mp3 tags. 
This tool is based off of Otavio Ehrenberger's tutorial <a href="https://www.freecodecamp.org/news/download-trim-mp3-from-youtube-with-python/">"How to Download and Trim MP3s from YouTube with Python"</a> on Free Code camp. It uses <a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a> instead of <a href="https://github.com/ytdl-org/youtube-dl">youtube-dl</a> among other changes. It works on any site that yt-dlp would.

## How to install this project

1. Clone this repo
2. Install dependencies

<!-- MANPAGE: BEGIN EXCLUDED SECTION -->
    pip install -r requirements.txt

<!-- MANPAGE: END EXCLUDED SECTION -->
## How to run this project

1. Add your URLs to the input.txt file. Each line is a separate URL.
2. Run the tool with the desired options.

<!-- MANPAGE: BEGIN EXCLUDED SECTION -->
    python run.py [OPTIONS] /path/to/save/videos

<!-- MANPAGE: END EXCLUDED SECTION -->

## General Options:
    -h, --help                      Print this help text and exit
    -folder_path                       Destination folder path to save files
    -S, --silent                    Silent mode, no user prompts    

## Find a bug?

If you found an issue or would like to submit an improvement to this project, please submit an issue using the issues tab above. If you would like to submit a PR with a fix, reference the issue you created!

## Known issues

This is a work in progress. Known issues will go here.

## Like this project?

Please share it.

## FAQ

In progress.