# -*- coding: utf-8 -*-
import pickle as pickle
import pandas as pd
import csv


input_file = "/home/obayashi/Projects/obayashi_practice/3.OD_predict/predict_result/cycle2_1/cycle1_xy.csv" #file_path you want to do post-processing
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
    if j-i < 20:
        for k in range(i+1,j):
            Class=dict_from_csv[str(i)][-1]
            print(Class)
            dict_from_csv[str(k)] = ['0']*22 + ['{}'.format(Class)]
    if j-i >=20:
        for k in range(i+1,j):
            dict_from_csv[str(k)] = ['0']*22 + ['I']

print(undetected_frame)
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
output_file = 'train.csv'
with open(output_file, 'a') as csv_file: 
    writer = csv.writer(csv_file,delimiter=',')
    writer.writerows(List)
