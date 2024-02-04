import cv2
import os

path = os.getcwd() + "/input_data/"

# uses yolo weights to detect coco objects in input image, draws bounding boxes around objects and saves result
# outputs boolean flag if a tractor (car or truck in coco) is detected or not
def detect():
    if not os.path.exists(path + "/original/"):
        os.makedirs(path + "/original/")

    filelist = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]  # ignore folders
    for filename in filelist:
        # skip augmented images, info.txt and the script itself
        if filename.find(".txt") != -1 or filename.find("coco") != -1 or filename.find("tsr") != -1:
            continue
        print(filename)

        img = cv2.imread(path + filename)

        # COCO DETECTION
        with open("coco.names", 'r') as f:
            classes = f.read().splitlines()

        net = cv2.dnn.readNetFromDarknet("yolov4.cfg", "yolov4.weights")

        model = cv2.dnn_DetectionModel(net)
        model.setInputParams(scale=1 / 255, size=(416, 416), swapRB=True)
        classIds, scores, boxes = model.detect(img, confThreshold=0.5, nmsThreshold=0.4)

        detected_classes = []
        for (classId, score, box) in zip(classIds, scores, boxes):
            cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), color=(0, 0, 255), thickness=2)

            text = '%s: %.2f' % (classes[classId], score)
            cv2.putText(img, text, (box[0], box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, color=(0, 0, 0), thickness=2)

            detected_classes.append(classes[classId] + ": " + str(round(100 * score, 0))[:-2] + "%")
        print(detected_classes)

        cv2.imwrite(path + filename[:-4] + "_coco.jpg", img)

        # write txt
        if filename.find("sev") != -1:
            f = open(path + filename[:-4] + ".txt", "r")
            lines = f.readlines()
            f.close()
        f = open(path + filename[:-4] + "_coco.txt", "w")
        for item in detected_classes:
            f.write(item + "\n")
        if filename.find("sev") != -1:
            for line in lines:
                f.write(line)
        f.close()

        # TS DETECTION
        img = cv2.imread(path + filename)

        with open("classes.names", 'r') as f:
            classes = f.read().splitlines()

        net = cv2.dnn.readNetFromDarknet("yolov4-ts2.cfg", "yolov4-ts2_best.weights")

        model = cv2.dnn_DetectionModel(net)
        model.setInputParams(scale=1 / 255, size=(416, 416), swapRB=True)
        classIds, scores, boxes = model.detect(img, confThreshold=0.5, nmsThreshold=0.4)

        detected_classes = []
        for (classId, score, box) in zip(classIds, scores, boxes):
            cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), color=(0, 0, 255), thickness=2)

            text = '%s: %.2f' % (classes[classId], score)
            cv2.putText(img, text, (box[0], box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, color=(0, 0, 0), thickness=2)

            detected_classes.append(classes[classId] + ": " + str(round(100 * score, 0))[:-2] + "%")
        print(detected_classes)

        cv2.imwrite(path + filename[:-4] + "_tsr.jpg", img)

        # write txt
        if filename.find("sev") != -1:
            f = open(path + filename[:-4] + ".txt", "r")
            lines = f.readlines()
            f.close()
        f = open(path + filename[:-4] + "_tsr.txt", "w")
        for item in detected_classes:
            f.write(item + "\n")
        if filename.find("sev") != -1:
            for line in lines:
                f.write(line)
        f.close()

        if filename.find("sev") != -1:
            os.rename(path + filename[:-4] + ".txt", path + "/original/" + filename[:-4] + ".txt")
        os.rename(path + filename, path + "/original/" + filename)

        # cv2.imshow('Image', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    return
