import imgaug.augmenters as ia

NO_AUG = 0  # If 1: No augmentation takes place
experiment_number = 3
sequence = 1  # 1 for full comparison, 0 for rest
description = ""


def getExperimentSeq(i, j):
    global description

    if experiment_number == 1:
        if i == 0 and j != 0:
            seq = [
                ia.imgcorruptlike.Snow(severity=j)
            ]
        elif j == 0 and i != 0:
            seq = [
                ia.imgcorruptlike.SpeckleNoise(severity=i)
            ]
        elif j != 0 and i != 0:
            seq = [
                ia.imgcorruptlike.SpeckleNoise(severity=i),
                ia.imgcorruptlike.Snow(severity=j)
            ]
        else:
            seq = []

        description = "Filters: DefocusBlur_" + str(i) + ", Snow_" + str(j)
        return seq

    elif experiment_number == 2:
        if i == 0 and j != 0:
            seq = [
                ia.imgcorruptlike.Snow(severity=j)
            ]
        elif j == 0 and i != 0:
            seq = [
                ia.imgcorruptlike.SpeckleNoise(severity=i)
            ]
        elif j != 0 and i != 0:
            seq = [
                ia.imgcorruptlike.SpeckleNoise(severity=i),
                ia.imgcorruptlike.Snow(severity=j)
            ]
        else:
            seq = []

        description = "Filters: DefocusBlur_" + str(i) + ", Snow_" + str(j)
        return seq

    if experiment_number == 3:
        seq = []
        if i == 0:
            description = "Filter: Snow_" + str(j)
            if j != 0:
                seq = [ia.imgcorruptlike.Snow(severity=j)]
        elif i == 1:
            description = "Filter: Fog_" + str(j)
            if j != 0:
                seq = [ia.imgcorruptlike.Fog(severity=j)]
        elif i == 2:
            description = "Filter: Frost_" + str(j)
            if j != 0:
                seq = [ia.imgcorruptlike.Frost(severity=j)]
        elif i == 3:
            description = "Filter: Splatter_" + str(j)
            if j != 0:
                seq = [ia.imgcorruptlike.Spatter(severity=j)]
        elif i == 4:
            description = "Filter: Brightness_" + str(j)
            if j != 0:
                seq = [ia.imgcorruptlike.Brightness(severity=j)]
        elif i == 5:
            description = "Filter: Blur_" + str(j)
            if j != 0:
                seq = [ia.imgcorruptlike.DefocusBlur(severity=j)]

        return seq

    elif experiment_number == 4:
        seq = [
            ia.imgcorruptlike.Fog(severity=3)
            ]
        return seq
