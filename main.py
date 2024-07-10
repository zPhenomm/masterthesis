# Author: Max Hannawald
# Controller for the analysis pipeline.

import full_plotting
import detector
import augmentation

augmentation.augment()
detector.detect()
full_plotting.sortResults()
full_plotting.prepare_data()
