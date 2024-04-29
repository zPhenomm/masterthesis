import matplotlib.pyplot as plt
import os
import seaborn as sns
import numpy as np
import config
import shutil

input_path = config.INPUT_PATH
output_path = config.OUTPUT_PATH

spots = ["0-0", "0-1", "0-2", "0-3", "0-4", "0-5", "1-0", "1-1", "1-2", "1-3", "1-4", "1-5", "2-0", "2-1", "2-2", "2-3",
         "2-4", "2-5", "3-0", "3-1", "3-2", "3-3", "3-4", "3-5", "4-0", "4-1", "4-2", "4-3", "4-4", "4-5", "5-0", "5-1",
         "5-2", "5-3", "5-4", "5-5"]

weather_names = config.WEATHER_NAMES

# select plot types
avg_plot = 1
violin = 1
heatmap = 1
derivative_heatmap = 1
average_weather = 1
# idv_heatmap = 0
# idv_plot = 0
show = 0  # show plots


def sortResults():
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if not os.path.exists(output_path + "coco_results/"):
        os.makedirs(output_path + "coco_results/")
    if not os.path.exists(output_path + "tsr_results/"):
        os.makedirs(output_path + "tsr_results/")
    if not os.path.exists(output_path + "plots/"):
        os.makedirs(output_path + "plots/")

    itemlist = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))]  # ignore folders

    for i in range(0, len(itemlist)):
        name = itemlist[i]
        if name.find("coco") != -1:
            shutil.copy2(input_path + name, output_path + "coco_results/" + name)  # need to use shutil here for Docker mounting
            os.remove(input_path + name)
        elif name.find("tsr") != -1:
            shutil.copy2(input_path + name, output_path + "tsr_results/" + name)
            os.remove(input_path + name)


def prepare_data():
    global input_path
    global modified_list

    cocolist = []
    tsrlist = []
    truthimg_coco = []
    truthimg_tsr = []

    # find the truthimages in the output
    for file in os.listdir(output_path + "coco_results/"):
        if file.find("sev") == -1 and file.find(".txt") != -1:
            truthimg_coco.append(file)
        elif file.find("sev") != -1 and file.find("coco") != -1 and file.find(".txt") != -1:
            cocolist.append(file)
    truthimg_coco.sort()
    cocolist.sort()

    for file in os.listdir(output_path + "tsr_results/"):
        if file.find("sev") == -1 and file.find(".txt") != -1:
            truthimg_tsr.append(file)
        elif file.find("sev") != -1 and file.find("tsr") != -1 and file.find(".txt") != -1:
            tsrlist.append(file)
    truthimg_tsr.sort()
    tsrlist.sort()

    # coco analysis
    mode = "coco_results/"
    sequence = []
    index = ["car", "person"]
    true_values_coco = [[], []]
    full_dev_coco = [[], []]
    plotlist = []

    for i, img in enumerate(truthimg_coco):
        sep = "_coco"
        stripped = truthimg_coco[i].split(sep, 1)[0]
        pattern = f"{stripped}_"
        # add list of all augmentations of one image to list
        sequence.append([x for x in tsrlist if x.startswith(pattern)])

        # save ground truth values of persons and cars
        true_values_coco[0].append(readInValues("car", truthimg_coco[i], mode))
        true_values_coco[1].append(readInValues("person", truthimg_coco[i], mode))

        # calculate deviations of images to ground truth
        for pos in range(0, len(true_values_coco)):
            if true_values_coco[pos][i]:
                values, deviation = calculateDeviations(sequence, i, index[pos], true_values_coco[pos], mode)
                plotlist.append([deviation, index[pos]])
                full_dev_coco[pos].append(deviation)

        # if idv_plot:
        #     plot(plotlist, img)
        # if idv_heatmap:
        #     individual_heatmap(plotlist, img)
        # plotlist = []

    # create violin plots
    if violin:
        for i in range(0, len(index)):
            format_violin(full_dev_coco[i], index[i])

    # create violin and heatmap plots with avg bad conditions
    if average_weather:
        for i in range(0, len(index)):
            avg_weather(full_dev_coco[i], index[i])

    # create heatmap of averages
    if heatmap:
        for i in range(0, len(index)):
            format_heatmap(full_dev_coco[i], index[i], 0)

    # create heatmap derivatives of averages
    if derivative_heatmap:
        for i in range(0, len(index)):
            format_heatmap(full_dev_coco[i], index[i], 1)

    # create plot of average deviations
    if avg_plot:
        for i in range(0, len(index)):
            plot_avg(full_dev_coco[i], index[i])

    # tsr analysis
    mode = "tsr_results/"
    sequence = []
    modified_list = [[], [], [], [], [], [], []]
    index = ["give_way", "priority_road", "prohibitory", "mandatory", "danger", "stop", "prohibitory_end"]
    true_values_tsr = [[], [], [], [], [], [], []]
    full_dev_tsr = [[], [], [], [], [], [], []]
    plotlist = []

    for i, img in enumerate(truthimg_tsr):
        sep = "_tsr"
        stripped = truthimg_tsr[i].split(sep, 1)[0]
        pattern = f"{stripped}_"
        # add list of all augmentations of one image to list
        sequence.append([x for x in tsrlist if x.startswith(pattern)])

        # save ground truth values of traffic signs
        true_values_tsr[0].append(readInValues("give_way", truthimg_tsr[i], mode))
        true_values_tsr[1].append(readInValues("priority_road", truthimg_tsr[i], mode))
        true_values_tsr[2].append(readInValues("prohibitory", truthimg_tsr[i], mode))
        true_values_tsr[3].append(readInValues("mandatory", truthimg_tsr[i], mode))
        true_values_tsr[4].append(readInValues("danger", truthimg_tsr[i], mode))
        true_values_tsr[5].append(readInValues("stop", truthimg_tsr[i], mode))
        true_values_tsr[6].append(readInValues("prohibitory_end", truthimg_tsr[i], mode))

        # calculate deviations of images to ground truth
        for pos in range(0, len(true_values_tsr)):
            if true_values_tsr[pos][i]:
                values, deviation = calculateDeviations(sequence, i, index[pos], true_values_tsr[pos], mode)
                plotlist.append([deviation, index[pos]])
                full_dev_tsr[pos].append(deviation)

        # if idv_plot:
        #     plot(plotlist, img)
        # if idv_heatmap:
        #     individual_heatmap(plotlist, img)
        # plotlist = []

    # create violin plots
    if violin:
        for i in range(0, len(index)):
            format_violin(full_dev_tsr[i], index[i])

    # create violin and heatmap plots with avg bad conditions
    if average_weather:
        for i in range(0, len(index)):
            avg_weather(full_dev_tsr[i], index[i])

    # create heatmap of averages
    if heatmap:
        for i in range(0, len(index)):
            format_heatmap(full_dev_tsr[i], index[i], 0)

    # create heatmap derivatives of averages
    if derivative_heatmap:
        for i in range(0, len(index)):
            format_heatmap(full_dev_tsr[i], index[i], 1)

    # create plot of average deviations
    if avg_plot:
        for i in range(0, len(index)):
            plot_avg(full_dev_tsr[i], index[i])

    if show:
        plt.show()


# this method calculates the deviation of an augmentation sequence of an image of a specified class (car, person,..)
def calculateDeviations(sequence, loopindex, obj, true_values, mode):
    values = []
    deviation = []
    for j, item in enumerate(sequence[loopindex]):
        values.append(readInValues(obj, item, mode))

        while len(true_values[loopindex]) > len(values[j]):  # in case of no detections add 0 as flags
            values[j].append(0)
        # calc deviations
        dev = 0
        for k in range(0, len(true_values[loopindex])):
            if values[j][k] == 0:
                dev += 1
            else:
                if values[j][k] < true_values[loopindex][k]:
                    dev += round(1 - values[j][k] / true_values[loopindex][k], 2)
                else:
                    dev += round(1 - true_values[loopindex][k] / values[j][k], 2)
        dev = round(dev / len(values[j]), 2)
        deviation.append(dev)

    return values, deviation


# this helper method reads in the values of a specified class (car, person,..) in a specified txt file (item)
def readInValues(obj, item, mode):

    with open(output_path + mode + item) as f:
        lines = f.readlines()
        sep = obj + ":"
        values = ([round((int(x[len(sep):-2])) * 0.01, 2) for x in lines if sep in x])
        if obj == "car":  # trucks und buses are cars as well
            sep = "truck:"
            tmp = ([round((int(x[len(sep):-2])) * 0.01, 2) for x in lines if sep in x])
            values.extend(tmp)
            sep = "bus:"
            tmp = ([round((int(x[len(sep):-2])) * 0.01, 2) for x in lines if sep in x])
            values.extend(tmp)
    f.close()

    return values


# plots the deviations of a specific class and image
def plot(plotlist, img):
    ticks = np.arange(36)

    for i, item in enumerate(plotlist):
        plt.figure(figsize=(13, 6))
        plt.plot(item[0], marker='o')
        plt.title(item[1] + " " + str(img)[:-4])
        plt.xticks(ticks, spots)
        ax = plt.gca()
        ax.set_ylim([0, 1.1])
        plt.xlabel("Augmentation")
        plt.ylabel("Abweichung")


# plots the deviations for each augmentation over all images as violin plots
def format_violin(lst, name):
    if not lst:
        return

    format = []
    tmp = []

    for i in range(0, len(lst[0])):
        for j in range(0, len(lst)):
            tmp.append(lst[j][i])
        format.append(tmp)
        tmp = []

    fig, axs = plt.subplots(2, 3, sharey=True)
    fig.suptitle("Verteilung Abweichungen Klasse " + name)
    plot_layout = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
    count = 0
    for i in range(0, len(lst[0]), config.SEVERITY_NUMBER):
        axs[plot_layout[count]].violinplot(format[i:i+config.SEVERITY_NUMBER], showmedians=True, showextrema=False)
        axs[plot_layout[count]].set_xticks([1, 2, 3, 4, 5, 6], spots[i:i+config.SEVERITY_NUMBER])
        axs[plot_layout[count]].set_ylim([0, 1.1])
        axs[plot_layout[count]].set_xlabel(weather_names[count])
        axs[plot_layout[count]].set_ylabel("deviation")
        count += 1
    plt.tight_layout()
    plt.savefig(output_path + "plots/violin_" + name + ".png")


def avg_weather(lst, name):

    if not lst:
        return

    format = []
    format_x = []
    tmp = []
    sum = 0

    for i in range(0, config.SEVERITY_NUMBER):
        for j in range(0, len(lst)):
            for k in range(0, len(lst[0]), config.SEVERITY_NUMBER):
                sum += lst[j][i+k]
            sum = sum / config.SEVERITY_NUMBER
            tmp.append(sum)
            sum = 0
        format.append(tmp)
        tmp = []

    plt.figure()
    plt.violinplot(format)
    plt.title("Verteilung Abweichungen bei durchschnittlichen Wettereffekten Klasse " + name, fontsize=10)
    plt.xticks([1, 2, 3, 4, 5, 6], ["0", "1", "2", "3", "4", "5"])
    ax = plt.gca()
    ax.set_ylim([0, 1.1])
    plt.xlabel("Wetter Intensität")
    plt.ylabel("Abweichung")
    plt.savefig(output_path + "plots/avg_weather_violin_" + name + ".png")

    # format violin plot for heatmap
    sum = 0
    for i in range(0, len(format)):
        for j in range(0, len(format[i])):
            sum += format[i][j]
        sum = round(sum / len(format[i]), 2)
        format[i] = sum
        sum = 0

    prev = 0
    for i in range(0, len(format)):
        format_x.append(round(format[i] - prev, 2))
        prev = format[i]

    format = [format]
    format_x = [format_x]
    plt.figure()
    cmap = sns.cm.rocket_r
    y_label = [""]
    ax = sns.heatmap(format, cmap=cmap, yticklabels=y_label, vmin=0, vmax=1, annot=True, fmt=".2f")
    plt.title("Abweichungen bei durchschnittlichen Wettereffekten Klasse " + name, fontsize=10)
    plt.xlabel("Wetter Intensität")
    plt.savefig(output_path + "plots/avg_weather_heatmap_" + name + ".png")

    plt.figure()
    cmap = sns.cm.rocket_r
    y_label = [" "]
    ax = sns.heatmap(format_x, cmap=cmap, yticklabels=y_label, vmin=0, vmax=1, annot=True, fmt=".2f")
    plt.title("Änderungsrate Abweichungen bei durchschnittlichen Wettereffekten Klasse " + name, fontsize=9)
    plt.xlabel("Wetter Intensität")
    plt.savefig(output_path + "plots/avg_weather_heatmap_change_" + name + ".png")


# plots the average deviations over all images as a heatmap
def format_heatmap(lst, name, flag):

    if not lst:
        return

    avg_deviation = []
    for i in range(0, len(lst[0])):
        sum = 0
        for j in range(0, len(lst)):
            sum += lst[j][i]
        avg_deviation.append(round(sum/len(lst), 3))

    # change format of list for heatmap
    format = [[], [], [], [], [], []]
    for j in range(0, config.SEVERITY_NUMBER):
        for k in range(0, len(lst[0]), config.SEVERITY_NUMBER):
            format[j].append(avg_deviation[j + k])

    # calculate derivative of heatmap entries in y-direction, if selected
    format_y = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
    format_x = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
    #format_y = [[0] * 6] * 6  this should produce the same results but for some reason it doesnt
    #format_x = [[0] * 6] * 6
    #format_y = format.copy()  this should produce the same results but for some reason it doesnt
    #format_x = format.copy()
    if flag:
        last_coordinate = (0, 0)
        for i in range(0, config.SEVERITY_NUMBER):
            for j in range(0, config.SEVERITY_NUMBER):
                m = round((format[j][i] - last_coordinate[1]), 3)
                last_coordinate = (j + 1, format[j][i])
                format_y[j][i] = m
            last_coordinate = (0, 0)

    format = list(map(list, zip(*format)))
    # format_x = list(map(list, zip(*format_x)))
    format_y = list(map(list, zip(*format_y)))

    plt.figure()
    cmap = sns.cm.rocket_r
    x_label = ["0", "1", "2", "3", "4", "5"]
    y_label = weather_names
    if flag:
        ax = sns.heatmap(format_y, xticklabels=x_label, yticklabels=y_label, cmap=cmap, vmin=0, vmax=1, annot=True, fmt=".3f")
        plt.title("Änderungsrate Abweichungen Klasse " + name)

    else:
        ax = sns.heatmap(format, xticklabels=x_label, yticklabels=y_label, cmap=cmap, vmin=0, vmax=1, annot=True, fmt=".3f")
        plt.title("Durchschnittliche Abweichungen Klasse " + name)

    #ax.invert_yaxis()
    plt.xlabel("Wetter Intensität")
    plt.ylabel("Wetter Effekt")
    if flag:
        plt.savefig(output_path + "plots/heatmap_change_" + name + ".png")
    else:
        plt.savefig(output_path + "plots/heatmap_" + name + ".png")


# plots the deviations of a specific class and image as a heatmap
def individual_heatmap(lst, img):

    for idx, item in enumerate(lst):
        format = [[], [], [], [], [], []]
        for j in range(0, config.SEVERITY_NUMBER):
            format[j].append(item[0][j])
            format[j].append(item[0][j+6])
            format[j].append(item[0][j+12])
            format[j].append(item[0][j+18])
            format[j].append(item[0][j+24])
            format[j].append(item[0][j+30])

        plt.figure()
        plt.title(item[1] + " " + str(img)[:-4])
        cmap = sns.cm.rocket_r
        x_label = ["1", "2", "3", "4", "5", "6"]
        y_label = ["1", "2", "3", "4", "5", "6"]
        ax = sns.heatmap(format, xticklabels=x_label, yticklabels=y_label, cmap=cmap, vmin=0, vmax=1)
        ax.invert_yaxis()
        plt.xlabel("Wetter Intensität")
        plt.ylabel("Wetter Effekt")


# plots the average deviations over all images of a specific class
def plot_avg(lst, img):

    if not lst:
        return

    avg_deviation = []
    for i in range(0, len(lst[0])):
        sum = 0
        for j in range(0, len(lst)):
            sum += lst[j][i]
        avg_deviation.append(sum / len(lst))

    plt.figure(figsize=(13, 6))
    ticks = np.arange(36)
    plt.plot(avg_deviation, marker='o')
    plt.title("Durchschnittliche Abweichungen der Klasse " + img)
    plt.xticks(ticks, spots)
    ax = plt.gca()
    ax.set_ylim([0, 1.1])
    plt.xlabel("Augmentation")
    plt.ylabel("Abweichung")
    plt.savefig(output_path + "plots/avg_dev_" + img + ".png", bbox_inches='tight')
