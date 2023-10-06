import subprocess

input_file = "../input.txt"
process_script = "audio.py"

with open(input_file, 'r') as file:
    for line in file:
        line = line.strip()  # Remove leading/trailing whitespace and newline characters
        command = ['python', process_script, line]

        try:
            subprocess.check_call(command)
        except subprocess.CalledProcessError:
            print(f"Error while processing: {line}")

print("Processing complete.")
