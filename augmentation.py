# Author: Max Hannawald
# This script augments images in the working directory with imgauglib
# and saves them in the same directory with a suffix specifying which experiment was done.
# Make sure the scripts sits in the same folder as the images, otherwise specify a new path.
# In aug_cfg you can specify what filters are to be applied and which number the experiment gets assigned.


import imgaug as ia
import imgaug.augmenters as iaa
import cv2
import aug_cfg
import os


def augment():
    if aug_cfg.NO_AUG:
        exit()

    ia.seed(1)
    path = os.getcwd() + "/input_data/"

    if aug_cfg.sequence:
        for i in range(0, 6):
            for j in range(0, 6):
                experiment_seq = aug_cfg.getExperimentSeq(i, j)
                seq = iaa.Sequential(experiment_seq, random_order=False)

                filelist = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]  # ignore folders
                for filename in filelist:
                    # skip augmented images, info.txt and the script itself
                    if filename.find(".jpg") == -1 or filename.find("_sev") != -1:
                        continue

                    filepath = os.path.join(path, filename)
                    img = cv2.imread(filepath)

                    image_aug = seq(image=img)
                    # save image with same name + _exp_x_sev_i_j
                    filepath = filepath[:-4] + "_exp_" + str(aug_cfg.experiment_number) + "_sev_" + str(i) + "_" + str(j) + ".jpg"
                    cv2.imwrite(filepath, image_aug)
                    filepath = filepath[:-4] + ".txt"
                    f = open(filepath, "w")
                    f.write(aug_cfg.description + "\n")
                    f.close()
                    print(filename + " " + str(i) + " " + str(j) + " augmentation done")

    else:
        experiment_seq = aug_cfg.getExperimentSeq(0, 0)
        seq = iaa.Sequential(experiment_seq, random_order=False)

        filelist = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]  # ignore folders
        for filename in filelist:

            # skip script and info file
            if filename.find(".py") != -1 or filename.find(".txt") != -1:
                continue

            filepath = os.path.join(path, filename)
            img = cv2.imread(filepath)

            image_aug = seq(image=img)
            # save image with same name + _exp_x_sev_i_j
            filepath = filepath[:-4] + ".jpg"
            cv2.imwrite(filepath, image_aug)
            print(filename + " augmentation done")
