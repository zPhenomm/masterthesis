import os
import random

path = os.getcwd() + "/GTSDB/"

filenames = os.listdir(path)

random.shuffle(filenames)
num_test_files = int(len(filenames) * 0.12)  # 12% test image ratio
test_filenames = filenames[:num_test_files]
train_filenames = filenames[num_test_files:]

with open('test.txt', 'w') as test_file:
    for filename in test_filenames:
        test_file.write(filename + '\n')

with open('train.txt', 'w') as train_file:
    for filename in train_filenames:
        train_file.write(filename + '\n')
