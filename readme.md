# youtube_audio

## A python tool to automatically download the audio of a YouTube video and set its mp3 tags. 
This tool is based off of Otavio Ehrenberger's tutorial <a href="https://www.freecodecamp.org/news/download-trim-mp3-from-youtube-with-python/">"How to Download and Trim MP3s from YouTube with Python"</a> on Free Code camp. It uses <a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a> instead of <a href="https://github.com/ytdl-org/youtube-dl">youtube-dl</a> among other changes. 

## How to install this project

1. Clone this repo
2. Install dependencies - pip install -r requirements.txt

## How to run this project

1. Add your URLs to the input.txt file. Each line is a separate URL.
2. Run the command - `python run.py [command line arguments] /path/to/save/videos`

## Command Line Arguments

`folder_path` - Destination folder path to save files
`-P`, `--prompt-user` - Prompt user for manual renaming
`-S`, `--silent` - Silent mode, no user prompts

## Find a bug?

If you found an issue or would like to submit an improvement to this project, please submit an issue using the issues tab above. If you would like to submit a PR with a fix, reference the issue you created!

## Known issues

This is a work in progress. Known issues will go here.

## Like this project?

Please share it.

## FAQ

In progress.