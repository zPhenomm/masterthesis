import os
import random

input_path = os.getcwd() + "/GTSDB/"

filenames = os.listdir(input_path)

random.shuffle(filenames)
num_test_files = int(len(filenames) * 0.12)  # 12% test image ratio
test_filenames = filenames[:num_test_files]
train_filenames = filenames[num_test_files:]

with open('resources/test.txt', 'w') as test_file:
    for filename in test_filenames:
        test_file.write("data/masterthesis/" + filename + '\n')

with open('resources/train.txt', 'w') as train_file:
    for filename in train_filenames:
        train_file.write("data/masterthesis/" + filename + '\n')
