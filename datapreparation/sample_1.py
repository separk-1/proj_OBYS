from DataPreprocessing import FrameExtraction
from DataPreprocessing import FormatRevision
from DataPreprocessing import Foldering

import os
ext_vidpath="/home/obayashi/Projects/proj_obayashi/codes/datapreparation/test_dataset/spot.mp4"
save_imgpath="/home/obayashi/Projects/proj_obayashi/codes/datapreparation/test_dataset/resized_spot/"
ext_imgpath="/home/obayashi/Projects/proj_obayashi/codes/datapreparation/test_dataset/resized_frog/"
save_vidpath="/home/obayashi/Projects/proj_obayashi/codes/datapreparation/test_dataset/new_frog.mp4"

## 1. Frame Extraction
FrameExtraction_1 = FrameExtraction(ext_vidpath, save_imgpath, ext_imgpath, save_vidpath)
FrameExtraction_1.video_to_frame()
#FrameExtraction_1.frame_to_video()

## 2. File Filter
'''
label_list = os.listdir("**dir")
image_list = os.listdir("**dir")
FormatRevision_1 = FormatRevision(label_list, image_list)
FormatRevision_1.file_filter()
'''

## 3. Foldering
'''
my_dir = "/home/obayashi/Projects/proj_obayashi/codes/datapreparation/test_dataset/"
case_name = "case_1"
train_dir = ["cycle_1", "cycle_2", "cycle_4"]
val_dir = ["cycle_3", "cycle_5"]
Foldering_1 = Foldering(my_dir, case_name, train_dir, val_dir)
Foldering_1.foldering()
'''