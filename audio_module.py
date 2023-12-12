import yt_dlp  # client to download from many multimedia portals
import glob  # directory operations
import os  # interface to os-provided info on files
from pydub import AudioSegment  # only audio operations


def newest_mp3_filename():
    # lists all mp3s in local directory
    list_of_mp3s = glob.glob('./*.mp3')
    # returns mp3 with highest timestamp value
    return max(list_of_mp3s, key=os.path.getctime)


def get_video_time_in_ms(video_timestamp):
    vt_split = video_timestamp.split(":")
    if len(vt_split) == 3:  # if in HH:MM:SS format
        hours = int(vt_split[0]) * 60 * 60 * 1000
        minutes = int(vt_split[1]) * 60 * 1000
        seconds = int(vt_split[2]) * 1000
    else:  # MM:SS format
        hours = 0
        minutes = int(vt_split[0]) * 60 * 1000
        seconds = int(vt_split[1]) * 1000
    # time point in milliseconds
    return hours + minutes + seconds


def get_trimmed(mp3_filename, initial, final=""):
    if not mp3_filename:
        # raise an error to immediately halt program execution
        raise Exception("No MP3 found in local directory.")
    # reads mp3 as a PyDub object
    sound = AudioSegment.from_mp3(mp3_filename)
    t0 = get_video_time_in_ms(initial)
    print("Beginning trimming process for file ", mp3_filename, ".\n")
    print("Starting from ", initial, "...")
    if len(final) > 0:
        print("...up to ", final, ".\n")
        t1 = get_video_time_in_ms(final)
        return sound[t0:t1]  # t0 up to t1
    return sound[t0:]  # t0 up to the end


# downloads yt_url to the same directory from which the script runs
def download_audio(yt_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_url])
