import os
import subprocess
import sys

def create_and_open_file(file_name):
    try:
        # Create the file if it doesn't exist
        if not os.path.isfile(file_name):
            open(file_name, 'w').close()

        # Open the file with Notepad
        subprocess.run(['notepad', file_name])
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: note <filename.extension> or note .")
        sys.exit(1)

    arg = sys.argv[1]

    if arg == '.':
        # Open Notepad without a file (for a new note)
        subprocess.run(['notepad'])
    else:
        # Create and open the specified file
        create_and_open_file(arg)

