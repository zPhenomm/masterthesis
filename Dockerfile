# Author: Max Hannawald
# This file creates the Docker image to run this project independent of the users' OS and system setup.

FROM ubuntu:22.04

# install Python, pip and libraries for OpenCV
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get install ffmpeg libsm6 libxext6  -y

# set the working directory in the container
WORKDIR /usr/src/app

# copy the current directory contents into the container at /usr/src/app
COPY . .

# install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# create directory for results to mount from local system
RUN mkdir /usr/src/app/results

# run main.py when the container launches
CMD ["python3", "main.py"]