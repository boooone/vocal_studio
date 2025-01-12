import os
import shutil 


ABLETON_MIDI_REMOTE_DIR = "/mnt/c/ProgramData/Ableton/Live 12 Suite/Resources/MIDI Remote Scripts/"

MIDI_REMOTE_SCRIPT_NAME = "AA_VocalStudio"

ABLETON_SERVER_DIR = "/home/boooone/projects/vocal_studio/src/ableton_midi_remote_server/"

# Helper to copy code from this source directory into Ableton Midi Remote scripts directory.


if __name__ == "__main__":
    # Check if Ableton install exists
    if not os.path.exists(ABLETON_MIDI_REMOTE_DIR):
        print("Ableton MIDI Remote Scripts directory not found at: " + ABLETON_MIDI_REMOTE_DIR)
        exit(1)

    midi_remote_script_dir = ABLETON_MIDI_REMOTE_DIR + MIDI_REMOTE_SCRIPT_NAME
    if not os.path.exists(midi_remote_script_dir):
        print("Ableton MIDI Remote Script directory not found at: " + midi_remote_script_dir + ", creating...")
        os.mkdir(midi_remote_script_dir)


    # Copy files
    for filename in os.listdir(ABLETON_SERVER_DIR):
        if filename.endswith(".py"):
            print("Copying: " + filename)
            shutil.copy(ABLETON_SERVER_DIR + filename, midi_remote_script_dir + "/" + filename)
