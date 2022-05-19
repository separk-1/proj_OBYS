import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import yaml
import pandas as pd
import argparse

from codes.functions.DataPreprocessing import Foldering
from codes.functions.DataPreprocessing import Foldering_Random
from codes.functions.DataPreprocessing import FrameExtraction
from codes.functions.DataPreprocessing import FormatRevision
from codes.functions import Augmentation

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mode', default = 'Foldering', type=str, required=False,
                        help="Set the datapreprocessing mode. Do not forget to configure config.yaml accordingly !")

with open('./config/config.yaml') as f:
    try:
      doc = yaml.load(f, Loader=yaml.FullLoader)
      args = parser.parse_args()
      data = doc['DATAPREPROCESSING'][args.mode]
    except yaml.YAMLError as exc:
        print(exc)
        
        
if args.mode == 'Foldering':
  train_list = [str(item) for item in data['train_dir'].split(',')]
  val_list = [str(item) for item in data['val_dir'].split(',')]
  
  Foldering_1 = Foldering(data['my_dir'], data['case_name'], train_list, val_list)
  Foldering_1.foldering()
  
  
elif args.mode == 'Foldering_Random':
  Foldering_Random_1 = Foldering_Random(my_dir = data['my_dir'],
                                        case_name= data['case_name'],
                                        threshold = data['threshold'])
  
  origin_df = Foldering_Random_1.origin_df()
  Random_df = Foldering_Random_1.Random_df()
  
  Foldering_Random_1.Set_Dir()
  Foldering_Random.save_plot(df = origin_df, threshold = data['threshold'], figpath=data['my_dir']+'%s/origin_plot.png'%(data['case_name'])) 
  Foldering_Random.save_plot(df = Random_df, threshold = data['threshold'], figpath=data['my_dir']+'%s_%s/random_plot.png'%(data['case_name'], data['threshold']))
  
  Foldering_Random_1.create_yaml()
  txt_filepath = data['my_dir']+"/%s.txt"%(data['case_name'])
  
  if os.path.exists(txt_filepath):
    os.remove(txt_filepath)
    
    
elif args.mode == "video_to_frame":
    FrameExtraction.video_to_frame(data['input_path'], data['output_path'])
    
    
elif args.mode == "frame_to_video":
    FrameExtraction.frame_to_video(data['input_path'], data['output_path'])
    
    
elif args.mode == 'FormatRevision':
  FormatRevision_1 = FormatRevision(data['label_list'], data['image_list'])
  FormatRevision_1.file_filter()
    
    
elif args.mode == 'Augmentation':
  Augmentation_1 = Augmentation(input_path = data['input_dir'], output_path = data['output_dir'], n = data['size'])
  Augmentation_1.Run()
  Augmentation_1.Annotation()
