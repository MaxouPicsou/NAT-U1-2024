from moviepy.editor import *
import os
from PIL import Image
import math


# PARAMETERS TO ADAPT
VIDEO_PATH = "1h_cut_webm.mp4"
ACTION_FILE_PATH = "1hour/action_file.csv"
FIRST_ACTION_TIME = 14

# Get file time creation
CREATION_TIME = os.path.getctime(VIDEO_PATH)

# Load video
video = VideoFileClip(VIDEO_PATH)
print("Duration(s):", video.duration)
print("FPS:", video.fps)

# Directory creation if it does not already exist
if not os.path.exists("data"):
    os.mkdir("data")

# Action number
i = 1

# Read action_file
with open(ACTION_FILE_PATH, 'r') as file:
    # Pass features line
    file.readline()

    # Get first action timestamp
    line = file.readline()
    last_timestamp = float(line.split(',')[-7])

    # Get first video frame
    frame = video.get_frame(FIRST_ACTION_TIME)
    new_img_path = "data/action_" + str(i) + "_" + line.split(',')[2] + ".jpg"
    new_img = Image.fromarray(frame)
    new_img.save(new_img_path)

    # Next action
    i += 1

    # Read through all the actions
    for line in file:
        # If line is not empty
        if len(line.split(',')) == 9:
            if line.split(',')[-7] != "":
                # Compute timestamp difference
                timestamp = float(line.split(',')[-7]) - last_timestamp + FIRST_ACTION_TIME
                print(line)
                print(math.floor(timestamp))

                # Get video frame
                frame = video.get_frame(math.floor(timestamp))
                new_img_path = "data/action_" + str(i) + "_" + line.split(',')[2] + ".jpg"
                new_img = Image.fromarray(frame)
                # Save video frame
                new_img.save(new_img_path)

        # Next action
        i += 1


