# Masterthesis Max Hannawald
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
- `input_data/`: Folder containing the input data for the analysis. After completion also contains the results.
- `resources/`: Folder containing files for running object detection and YOLOv4 training.
- `GTSDB/`: Dataset on which the traffic sign detector has been trained.

### Running the project with Docker:
- Build the image with: `docker build -t thesis .`
- To run the project: `docker run -it thesis`