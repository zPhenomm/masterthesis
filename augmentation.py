# Author: Max Hannawald
# This script augments images in the input folder with imgauglib and saves them in the same directory.
# In aug_cfg.py you can specify what filters are to be applied.

import imgaug as ia
import imgaug.augmenters as iaa
import cv2
import aug_cfg
import os
import config

input_path = config.INPUT_PATH


def augment():
    if config.NO_AUG:
        exit()

    ia.seed(1)

    for i in range(0, config.SEVERITY_NUMBER):
        for j in range(0, config.SEVERITY_NUMBER):
            experiment_seq = aug_cfg.getExperimentSeq(i, j)
            seq = iaa.Sequential(experiment_seq, random_order=False)

            filelist = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))]  # ignore folders
            for filename in filelist:
                # skip augmented images, info.txt and the script itself
                if filename.find(".jpg") == -1 or filename.find("_sev") != -1:
                    continue

                filepath = os.path.join(input_path, filename)
                img = cv2.imread(filepath)

                image_aug = seq(image=img)
                # save image with same name + _eff_x_sev_i_j
                filepath = filepath[:-4] + "_eff_" + str(i) + "_sev_" + str(j) + ".jpg"
                cv2.imwrite(filepath, image_aug)
                filepath = filepath[:-4] + ".txt"
                f = open(filepath, "w")
                f.write(aug_cfg.description + "\n")
                f.close()
                print(filename + " " + str(i) + " " + str(j) + " augmentation done")
