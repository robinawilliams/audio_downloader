import subprocess


def prompt_for_minutes_and_seconds(prompt):
    while True:
        timestamp = input(prompt)
        try:
            mm, ss = map(int, timestamp.split(':'))
            return mm, ss
        except ValueError:
            print("Invalid timestamp format. Please use 'mm:ss' format.")


def clip_mp3(input_file, output_file, start_time, end_time):
    start_timestamp = f"00:{start_time[0]:02d}:{start_time[1]:02d}"
    end_timestamp = f"00:{end_time[0]:02d}:{end_time[1]:02d}"

    ffmpeg_cmd = [
        "ffmpeg",
        "-i", input_file,
        "-ss", start_timestamp,
        "-to", end_timestamp,
        "-c:a", "copy",
        output_file,
    ]

    subprocess.run(ffmpeg_cmd)


if __name__ == "__main__":
    input_file = input("Enter the path to the input MP3 file: ")
    output_file = input("Enter the path for the output MP3 file: ")

    print("Enter the start timestamp (mm:ss):")
    start_time = prompt_for_minutes_and_seconds("Start time: ")
    print("Enter the end timestamp (mm:ss):")
    end_time = prompt_for_minutes_and_seconds("End time: ")

    clip_mp3(input_file, output_file, start_time, end_time)
    print("MP3 file has been clipped successfully.")
