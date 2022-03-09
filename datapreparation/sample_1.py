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
case_name = "0309_case_11" ##

my_dir = "/home/obayashi/data/cctv_video/train_data/"
train_data = my_dir+"%s.xlsx"%(case_name)
train_df = pd.read_excel(train_data)
train_dir = list(train_df[train_df['type'] == 'train']["cycle"])
val_dir = list(train_df[train_df['type'] == 'val']["cycle"])

Foldering_1 = Foldering(my_dir, case_name, train_dir, val_dir)
Foldering_1.foldering()



## 3.2 Random_Foldering
my_dir = "/home/obayashi/data/cctv_video/train_data/Case/"
case_name = "case_simple"
threshold = 100

Foldering_Random_1 = Foldering_Random(my_dir = my_dir,
                                      case_name= case_name,
                                      threshold = threshold)

origin_df = Foldering_Random_1.origin_df()
Foldering_Random.save_plot(df = origin_df, threshold = threshold, figpath=my_dir+'%s/simple_origin_plot.png'%(case_name)) 

Random_df = Foldering_Random_1.Random_df()
Foldering_Random_1.Set_Dir()
Foldering_Random.save_plot(df = Random_df, threshold = threshold, figpath=my_dir+'%s_%s/simple_random_plot.png'%(case_name, threshold))

