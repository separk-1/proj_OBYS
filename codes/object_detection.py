import pandas as pd
import argparse
import yaml
import os
import numpy as np
import pickle5 as pickle
import csv

parser = argparse.ArgumentParser()
parser.add_argument('--mode', default = 'prediction', type=str, required=False)
parser.add_argument('--data', default = '../config/config.yaml', type=str, required=False,)
args = parser.parse_args()

#load yaml
myyaml = args.data
with open(myyaml)as f:
    Doc = yaml.load(f, Loader=yaml.FullLoader)
    doc = Doc["OBJECT_DETECTION"]


def pkl_to_csv_ID(file_name, path, save_dir):
    with open(path + file_name+'.pkl', 'rb') as file:
        data = pickle.load(file)

    class_num = 11
    #checklist is for extracting keys in data dictionary
    checklist = list()
    Data={}
    small={}
    for keys in data:
        LList = [0]*class_num
        for j in data[keys]:
            js = j.split(" ")
            j_id = js[0]
            LList[int(j_id)] = 1
        Data[keys] = LList
        checklist.append(keys)
    checklist.sort()
    for i in range(len(checklist)-1):
        if (checklist[i+1] - checklist[i]) != 1:
            for i in range(checklist[i]+1, checklist[i+1]):
                small[i] = [0] * class_num
 
    for i in small:
        Data[i] = small[i]
    Last_dict = {}
    sorted_dict = sorted(Data.items())

    for i in sorted_dict:
        Last_dict[i[0]] = i[1]
    df = pd.DataFrame(Last_dict)
    df = df.transpose()
    df.rename(columns={0: 'drill_jumbo', 1: 'gunpowder_carrier', 2: 'work platform', 3: 'breaker', 4: 'excavator',
                   5: 'payloader', 6: 'dump_truck', 7: 'sprayer', 8: 'h_beam_holder', 9: 'mixer_truck', 10:'mortar_trolley_truck'},
          inplace=True)

    #2. modify the flickering 
    col_list = ["drill_jumbo","gunpowder_carrier","work platform","breaker","excavator","payloader","dump_truck","sprayer","h_beam_holder","mixer_truck","mortar_trolley_truck"]

    n = 30
    Dict = dict()
    for j in col_list:
        list_df = df[j].tolist()
        for i in range(len(list_df)):
              if list_df[i] ==1:
                pass
              else:
                  if i<=n:
                      pass
                  elif i>=(len(list_df)-n-1):
                      pass
                  else:
                      front_list = list_df[i-n:i]
                      last_list = list_df[i:i+n]
                      if list_df[i-1] == 0:
                         pass
                      else:
                          if 1 in front_list and 1 in last_list:
                              list_df[i]=1
                          else:
                              pass
        Dict[j] = list_df

    df2 = pd.DataFrame(Dict)
    df2.to_csv(save_dir+file_name+'_ID.csv')

def pkl_to_csv_xy(file_name, path, save_dir):

    with open(path + file_name+'.pkl', 'rb') as file:
        data = pickle.load(file)
    class_num = 11
    for keys in data:
        LList = ["0"]*class_num*2
        for j in data[keys]:
            js = j.split(" ")
            j_id = js.pop(0)
            LList[2 * int(j_id)] = js[0]
            LList[2 * int(j_id)+1] = js[1]
        data[keys] = LList

    df = pd.DataFrame(data)
    df = df.transpose()
    coord = ["cx", "cy"]

    classes=["drill_jumbo", "gunpowder_carrier", "work platform", "breaker", "excavator", "payloader", "dump_truck", "sprayer", "h_beam_holder", "mixer_truck", "mortar_trolley_truck"]
    for i, cl in zip(range(0, class_num), classes):
        df.rename(columns={2*i: cl+"_"+coord[0], 2*i+1:cl+"_"+coord[1]},inplace=True)
    df=df.rename_axis('frame_num')

    df.to_csv(save_dir+file_name+'_xy.csv')
    return df

def xy_mod(xy_csv_file, file_name, path, save_dir):
    input_file = xy_csv_file
   
    df1 = pd.read_csv(input_file)
    df = pd.DataFrame(df1)
        
    col_list = ['frame_num','drill_jumbo_cx','drill_jumbo_cy','gunpowder_carrier_cx','gunpowder_carrier_cy','work platform_cx','work platform_cy','breaker_cx','breaker_cy', 'payloader_cx', 'payloader_cy', 'dump_truck_cx','dump_truck_cy','sprayer_cx','sprayer_cy','h_beam_holder_cx','h_beam_holder_cy','mixer_truck_cx','mixer_truck_cy','activity']
        
    ###csv to dict
    dict_from_csv = {}
    with open(input_file, mode='r') as inp:
        reader = csv.reader(inp)
        dict_from_csv = {rows[0]:rows[1:] for rows in reader}
    
    #add undetected frame
    undetected_frame = []
    frames = []
    for row_index, row in df1.iterrows():
        frames.append(row['frame_num'])
    for i in range(1, len(frames)):
        if frames[i] != frames[i-1]+1:
            undetected_frame.append([frames[i-1], frames[i]]) 
    for i,j in undetected_frame:
        i= int(i)
        j= int(j)
        if j-i < 20:
            for k in range(i+1,j):
                Class=dict_from_csv[str(i)][-1]
                dict_from_csv[str(k)] = ['0']*22 + ['{}'.format(Class)]
        if j-i >=20:
            for k in range(i+1,j):
                dict_from_csv[str(k)] = ['0']*22 + ['I']
    new_dict = {}
    for keys in dict_from_csv:
        if keys != 'frame_num':
            value = dict_from_csv[keys]
            new_dict[int(keys)] = value
        else:  
            pass
            
    sdict = sorted(new_dict.items())
    
    List = []
    Dict = {}
    col_list = ['frame_num','drill_jumbo_cx','drill_jumbo_cy','gunpowder_carrier_cx','gunpowder_carrier_cy','work platform_cx','work platform_cy','breaker_cx','breaker_cy', 'excavator_cx','excavator_cy','payloader_cx', 'payloader_cy', 'dump_truck_cx','dump_truck_cy','sprayer_cx','sprayer_cy','h_beam_holder_cx','h_beam_holder_cy','mixer_truck_cx','mixer_truck_cy','mortar_trolley_truck_cx','mortar_trolley_truck_cy','activity']
    List.append(col_list)
    for i, j in sdict:
        Dict[i] = j
        sublist = []
        sublist.append(str(i))
        for ii in j:
            sublist.append(ii)
        List.append(sublist)
    output_file = save_dir+file_name+'_xy_mod.csv'
    with open(output_file, 'a') as csv_file: 
        writer = csv.writer(csv_file,delimiter=',')
        writer.writerows(List)


if args.mode == 'training':
    os.chdir("../")
    mode = 'training'
    batch= doc[mode]['batch']
    epochs= doc[mode]['epochs']
    traindata=doc[mode]['traindata']
    pre_weights= doc[mode]['pre_weights']
    save_name= doc[mode]['save_name']
    save_dir=doc[mode]['save_dir']
    
    command1 = 'python ./codes/yolov5/train.py --batch '
    command1 += batch
    command1 += ' --epochs '
    command1 += epochs
    command1 += ' --data ' 
    command1 += traindata
    command1 += ' --weights '
    command1 += pre_weights
    command1 += ' --name '
    command1 += save_name
    command1 += ' --project '
    command1 += save_dir
    os.system(command1)

elif args.mode == 'prediction':
    mode = 'prediction'
    file_name= doc[mode]['file_name']
    detect_model= doc[mode]['detect_model']
    source=doc[mode]['source'] + file_name
    weights= doc[mode]['weights']
    conf= doc[mode]['conf']
    save_dir=doc[mode]['save_dir']
    save_name=file_name[:-4]
    
   
    command1 = 'CUDA_VISIBLE_DEVICES=0,1 python '
    command1 += detect_model
    command1 += ' --source '
    command1 += source
    command1 += ' --weights '
    command1 += weights
    command1 += ' --conf '
    command1 += conf
    command1 += ' --project '
    command1 += save_dir
    command1 += ' --name '
    command1 += save_name
    #command1 += ' --save-txt'
    
    os.system(command1)


elif args.mode == 'postprocessing':
    mode = 'postprocessing'
    
    path= doc[mode]['path']
    file_name= doc[mode]['file_name']
    save_dir= doc[mode]['save_dir']
    video_name = file_name.split('.')[0]
    
    pkl_to_csv_ID(video_name, path, save_dir)
    pkl_to_csv_xy(video_name, path, save_dir)
    
    xy_csv_file= save_dir+video_name+'_xy.csv'
    xy_mod(xy_csv_file, video_name, path, save_dir)

    
