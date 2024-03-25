import os
import cv2

input_path = os.getcwd() + "/GTSDB/"

filelist = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))]
for filename in filelist:
    if filename.find("txt") == -1 and filename.find("jpg") == -1:
        i = cv2.imread(input_path + filename)
        cv2.imwrite(input_path + filename[:-4] + ".jpg", i)
        os.remove(input_path + filename)
