## Masterthesis Max Hannawald
Development of a prototype to analyse the influence of weather on the automatic detection of objects in traffic.
### To get started:
Clone the master branch from the [repository](https://github.com/zPhenomm/masterthesis.git).

Make sure to have Git LFS installed on your system to download the .weights files for detection as they are larger than the limit for GitHub Repos.

### Repository Structure:
- `main.py`: Main script utilizing `augmentation.py`, `detector.py`, `full_plotting.py`, to augment testimages and to analyse and visualize the influence of the augmentation on the object detection.
- `aug_cfg.py` and `config.py`: Config scripts for augmentation, detection and plotting.
- `convert_images.py`: Script for converting the GTSDB images from `.ppm` to `.jpg`.
- `set_splitting`: Script for splitting the GTSDB dataset into train and test sets.
- `Dockerfile`: File for running the project with Docker.
- `input_data/`: Folder containing the input data for the analysis. The provided images are the same that are used in the analysis of this master thesis.
- `input_data/augmented/`: Created at runtime, contains all augmented images without object detection after completion.
- `results/`: Created at runtime, contains results after completion.
- `resources/`: Folder containing files for running object detection and YOLOv4 training.
- `GTSDB/`: Dataset on which the traffic sign detector has been trained.

### Running the project:
- Install Python (Version >= 3.10) and pip
- Install all requirements listed in `requirements.txt`
- Run `python3 main.py` in the terminal in the project directory with either the provided input files to verify the results of this thesis or with own dataset. Be aware that using the provided input the produced results require about 13GB of space.
- Clear results from project directory before running again to avoid filename conflicts

### Running the project with Docker:
- Install [Docker](https://www.docker.com) if it's not natively supported by your OS.
- Navigate in the terminal to the project folder in your filesystem.
- Build the image (~4GB): `docker build -t thesis .`
- Run the project and save results to a Docker volume: `docker run -it --name thesis-container -v thesis_results:/usr/src/app/results thesis`
- Shutdown the Docker container: `docker stop thesis-container && docker rm thesis-container`
- Copy the results to your system: `docker run --rm -v thesis_results:/usr/src/app/results -v /path/to/folder:/backup thesis cp -r /usr/src/app/results/. /backup`. Make sure to replace the `/path/to/folder` in the command with the desired output path on your system.
- Before running again remove the volume with the results: `docker volume rm thesis_results`