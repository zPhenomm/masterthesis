# Author: Max Hannawald
# Helper script to downscale the input images to ~1080p for the analysis. Not part of the analysis pipeline.

import cv2
import os

input_folder = "input_data/"
output_folder = "output/"
# make sure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
count = 1  # counter for naming
target_size = (1920, 1440)

# loop through files and resize
for file in files:
    try:
        file_path = os.path.join(input_folder, file)
        img = cv2.imread(file_path)
        if img is None:
            print(f"Failed to load {file}")
            continue

        img_resized = cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)  # resize the image
        new_filename = f"{count}.jpg"
        cv2.imwrite(os.path.join(output_folder, new_filename), img_resized)
        print(f"Resized and saved {new_filename}")
        count += 1
    except Exception as e:
        print(f"Unable to resize file {file}: {e}")
