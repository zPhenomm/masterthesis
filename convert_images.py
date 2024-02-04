import os
import cv2

path = os.getcwd() + "/GTSDB/"

filelist = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
for filename in filelist:
    if filename.find("txt") == -1 and filename.find("jpg") == -1:
        i = cv2.imread(path + filename)
        cv2.imwrite(path + filename[:-4] + ".jpg", i)
        os.remove(path + filename)