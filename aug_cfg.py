import imgaug.augmenters as ia

sequence = 1  # 1 for full comparison, 0 for rest
description = ""


def getExperimentSeq(i, j):
    global description

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
