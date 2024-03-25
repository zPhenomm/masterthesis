import cv2
import os
import time
import config

input_path = config.INPUT_PATH


# uses yolo weights to detect coco and tsr objects in input image, draws bounding boxes around objects and saves result
def detect():
    if not os.path.exists(input_path + "/augmented/"):
        os.makedirs(input_path + "/augmented/")

    filelist = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))]  # ignore folders
    for filename in filelist:
        # skip detected images, info.txt
        if filename.find(".txt") != -1 or filename.find("coco") != -1 or filename.find("tsr") != -1:
            continue
        print(filename)

        img = cv2.imread(input_path + filename)

        # COCO DETECTION
        with open("resources/coco.names", 'r') as f:
            classes = f.read().splitlines()

        net = cv2.dnn.readNetFromDarknet("resources/yolov4.cfg", "resources/yolov4.weights")

        model = cv2.dnn_DetectionModel(net)
        model.setInputParams(scale=1 / 255, size=(416, 416), swapRB=True)
        classIds, scores, boxes = model.detect(img, confThreshold=0.5, nmsThreshold=0.4)

        detected_classes = []
        for (classId, score, box) in zip(classIds, scores, boxes):
            cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), color=(101, 255, 0), thickness=5)

            text = '%s: %.2f' % (classes[classId], score)
            cv2.putText(img, text, (box[0], box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 2, color=(255, 255, 255), thickness=5)

            detected_classes.append(classes[classId] + ": " + str(round(100 * score, 0))[:-2] + "%")
        print(detected_classes)

        cv2.imwrite(input_path + filename[:-4] + "_coco.jpg", img)

        time.sleep(0.2)

        # write txt
        if filename.find("sev") != -1:
            f = open(input_path + filename[:-4] + ".txt", "r")
            lines = f.readlines()
            f.close()
        f = open(input_path + filename[:-4] + "_coco.txt", "w")
        for item in detected_classes:
            f.write(item + "\n")
        if filename.find("sev") != -1:
            for line in lines:
                f.write(line)
        f.close()

        time.sleep(0.2)

        # TS DETECTION
        img = cv2.imread(input_path + filename)

        with open("resources/classes.names", 'r') as f:
            classes = f.read().splitlines()

        net = cv2.dnn.readNetFromDarknet("resources/yolov4-ts2.cfg", "resources/yolov4-ts2_best.weights")

        model = cv2.dnn_DetectionModel(net)
        model.setInputParams(scale=1 / 255, size=(416, 416), swapRB=True)
        classIds, scores, boxes = model.detect(img, confThreshold=0.5, nmsThreshold=0.4)

        detected_classes = []
        for (classId, score, box) in zip(classIds, scores, boxes):
            cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), color=(101, 255, 0), thickness=5)

            text = '%s: %.2f' % (classes[classId], score)
            cv2.putText(img, text, (box[0], box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 2, color=(255, 255, 255), thickness=5)

            detected_classes.append(classes[classId] + ": " + str(round(100 * score, 0))[:-2] + "%")
        print(detected_classes)

        cv2.imwrite(input_path + filename[:-4] + "_tsr.jpg", img)

        time.sleep(0.2)

        # write txt
        if filename.find("sev") != -1:
            f = open(input_path + filename[:-4] + ".txt", "r")
            lines = f.readlines()
            f.close()
        f = open(input_path + filename[:-4] + "_tsr.txt", "w")
        for item in detected_classes:
            f.write(item + "\n")
        if filename.find("sev") != -1:
            for line in lines:
                f.write(line)
        f.close()

        time.sleep(0.2)

        if filename.find("sev") != -1:
            os.rename(input_path + filename[:-4] + ".txt", input_path + "/augmented/" + filename[:-4] + ".txt")
        if not (filename.find("sev") == -1 and filename.find(".txt") == -1):  # keep original images in input folder
            os.rename(input_path + filename, input_path + "/augmented/" + filename)

        time.sleep(0.2)

        # cv2.imshow('Image', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    return
