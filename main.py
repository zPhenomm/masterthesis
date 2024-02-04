import full_plotting
import detector
import aug_cfg
import augmentation

augmentation.augment()
detector.detect()
full_plotting.sortResults()
full_plotting.prepare_data()
