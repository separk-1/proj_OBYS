import os
import pandas as pd
import json
import pickle5 as pickle

def OD_pkl_to_csv_mod(file_name, path):
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

            #for the missed frame, add frame with [0]*10 list value
            for i in range(checklist[i]+1, checklist[i+1]):
            #i 4001~12000
                #print(i)
                small[i] = [0] * class_num
                #added key of data
                #print(i,data[i])
    #print(small)
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
        print(list_df)
        #df[j]_columnlist
        for i in range(len(list_df)):
            #list_df = lisf of each column
            if list_df[i] ==1:
                pass
            else:
                #i>=n
                if i<=n:
                    pass
                elif i>=(len(list_df)-n-1):
                    pass
                else:
                    front_list = list_df[i-n:i]
                    last_list = list_df[i:i+n]
                    if list_df[i-1] == 0:
                       pass
                    #print(list_df[i-n:i],list_df[i:i+n])

                    else:

                        if 1 in front_list and 1 in last_list:

                            list_df[i]=1

                        else:
                            pass
        Dict[j] = list_df


    #make new dictionary with modified version
    df2 = pd.DataFrame(Dict)
    df2.to_csv('/home/obayashi/Projects/obayashi_practice/3.OD_predict/predict_result/cycle2_1/'+file_name+'_mod.csv')