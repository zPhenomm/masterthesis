import os
import cv2

INPUT_PATH = os.getcwd() + "/input_data/"
OUTPUT_PATH = os.getcwd() + "/results/"

NO_AUG = False
SEVERITY_NUMBER = 6
WEATHER_NAMES = ["Schnee", "Nebel", "Frost", "Schmutz", "Überblendung", "Unschärfe"]

CONF_THRESH = 0.45

coco_net = cv2.dnn.readNetFromDarknet("resources/yolov4.cfg", "resources/yolov4.weights")
COCO_MODEL = cv2.dnn_DetectionModel(coco_net)
COCO_MODEL.setInputParams(scale=1 / 255, size=(416, 416), swapRB=True)

tsr_net = cv2.dnn.readNetFromDarknet("resources/yolov4-ts2.cfg", "resources/yolov4-ts2_best.weights")
TSR_MODEL = cv2.dnn_DetectionModel(tsr_net)
TSR_MODEL.setInputParams(scale=1 / 255, size=(416, 416), swapRB=True)
