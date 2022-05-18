# -*- coding: utf-8 -*-
import pickle as pickle
import pandas as pd

file_list=[1]

for file_name in file_list:
  with open("/home/obayashi/Projects/proj_obayashi/results/cycle_test_result/cycle2/cycle2.pkl", 'rb') as file:
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
  #class Î¶¨Ïä§???ÅÍ∏∞
  classes=["drill_jumbo", "gunpowder_carrier", "work platform", "breaker", "excavator", "payloader", "dump_truck", "sprayer", "h_beam_holder", "mixer_truck", "mortar_trolley_truck"]
  for i, cl in zip(range(0, class_num), classes):
      df.rename(columns={2*i: cl+"_"+coord[0], 2*i+1:cl+"_"+coord[1]},inplace=True)
  
  df=df.rename_axis('frame_num')
  # csvÎ°??Ä??
  Path = '/home/obayashi/Projects/obayashi_practice/3.OD_predict/predict_result/'
  df.to_csv(Path+file_name +'_xy.csv')
  print("csv file is saved!!")
  
  # excelÎ°??Ä??
  # df.to_excel('2021-08-25_00-00-00.xlsx')
  
