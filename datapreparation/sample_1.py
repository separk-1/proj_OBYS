from DataPreprocessing import FrameExtraction
from DataPreprocessing import FormatRevision
from DataPreprocessing import Foldering
from DataPreprocessing import Foldering_Random
import os

'''
## 1. Frame Extraction
ext_vidpath="/home/obayashi/Projects/proj_obayashi/codes/datapreparation/test_dataset/spot.mp4"
save_imgpath="/home/obayashi/Projects/proj_obayashi/codes/datapreparation/test_dataset/resized_spot/"
ext_imgpath="/home/obayashi/Projects/proj_obayashi/codes/datapreparation/test_dataset/resized_frog/"
save_vidpath="/home/obayashi/Projects/proj_obayashi/codes/datapreparation/test_dataset/new_frog.mp4"

FrameExtraction_1 = FrameExtraction(ext_vidpath, save_imgpath, ext_imgpath, save_vidpath)
FrameExtraction_1.video_to_frame()
#FrameExtraction_1.frame_to_video()
'''

## 2. File Filter
'''
label_list = os.listdir("**dir")
image_list = os.listdir("**dir")
FormatRevision_1 = FormatRevision(label_list, image_list)
FormatRevision_1.file_filter()
'''

## 3.1 Foldering
#Sample_MobaXterm
my_dir = "/home/obayashi/Projects/proj_obayashi/codes/datapreparation/test_dataset/"
case_name = "case_1"
train_dir = ["cycle_1", "cycle_2", "cycle_4"]
val_dir = ["cycle_3", "cycle_5"]
Foldering_1 = Foldering(my_dir, case_name, train_dir, val_dir)
Foldering_1.foldering()

#Sample_Local
my_dir = "./"
case_name = "case_cycle1"
train_dir = ["cycle1_1", "cycle1_2"]
val_dir = ["cycle1_3"]
Foldering_1 = Foldering(my_dir, case_name, train_dir, val_dir)
Foldering_1.foldering()

## 3.2 Random_Foldering

Foldering_Random_1 = Foldering_Random(case_name= "case_cycle1",
                                      threshold = 1000,
                                      txt_path='filenames.txt')

origin_df = Foldering_Random_1.origin_df()
#Foldering_Random_1.save_plot(df = origin_df, figpath='origin_plot.png')

Random_df = Foldering_Random_1.Random_df()
#Foldering_Random_1.save_plot(df = Random_df, figpath='random_plot.png')