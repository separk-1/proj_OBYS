import pandas as pd
import math
import argparse
import yaml
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def createFolder(directory):
  try:
    if not os.path.exists(directory):
      os.makedirs(directory)
  except OSError:
    print('Error: Creating directory. ' + directory)

def df_rolling_and_T(df, time):
  df_min = df.rolling(window=time).mean()
  df_min = df_min[(df_min.index%time==0) & (df_min.index!=0)]
  df_min_round = df_min.round(0).astype(int)
  index_list = [int(x*time/60) for x in range(1, math.floor(len(df)/time)+1)]
  df_min_round.index = index_list
  df_min_T = df_min_round.T
  return df_min_T

def making_timetable(input_dir, output_dir, interval):
  df = pd.read_csv(input_dir, index_col = 0)
  df_A = pd.DataFrame(df['activity'])
  df.drop(['activity'], axis = 1, inplace = True)

  columns = sorted(df_A['activity'].unique())
  for col in columns:
    col_list = list()
    for i in df_A.index:
      if df_A.at[i, 'activity'] == col:
        col_list.append(1)
      else:
        col_list.append(0)
    df_A[col] = col_list
  df_A.drop(['activity'], axis = 1, inplace = True)

  df_rolling_and_T(df, interval).to_csv(output_dir+'/timetable_equip_'+str(interval)+'.csv')
  df_rolling_and_T(df_A, interval).to_csv(output_dir+'/timetable_activity_'+str(interval)+'.csv')


#cycle time of each activity
def time_of_activity(input_data, output_dir, act_class):
    df = pd.read_csv(input_data)
    df.rename(columns={'Unnamed: 0': 'time'}, inplace=True)

    num_class = len(act_class)
    start = ord('A')
    for i in range(num_class):
        df.loc[df['activity']== chr(start),'activity'] = act_class[i]
        start+=1

    activity_column = df['activity'].tolist()
    act_time_list=[]

    for actclass in act_class:
        semi_list=[actclass]
        length= len(activity_column)
        for i in range(length):
            if activity_column[i] == actclass:
                if i == 0:
                    semi_list.append(i)
                elif i == length-1:
                    semi_list.append(i)
                    gap = semi_list[2] - semi_list[1]+1
                    semi_list.append(gap)
                    act_time_list.append(semi_list)
                elif activity_column[i-1] == actclass and activity_column[i+1] == actclass:
                    continue
                elif activity_column[i-1] == actclass and activity_column[i+1] != actclass:
                    semi_list.append(i)
                    gap = semi_list[2] - semi_list[1]+1
                    semi_list.append(gap)
                    act_time_list.append(semi_list)
                    semi_list=[actclass]
                elif activity_column[i-1] != actclass and activity_column[i+1] == actclass:
                    semi_list.append(i)
                elif activity_column[i-1] != actclass and activity_column[i+1] != actclass:
                    continue

    col= ['activity','start_time','end_time','gap']
    act_time_df = pd.DataFrame(act_time_list, columns=col)
    act_time_df.sort_values(by=['start_time'], axis=0, inplace = True)
    act_time_df.reset_index(drop = True, inplace = True)
    act_time_df.to_csv(output_dir+'/act_time.csv')

#counting_dumptruck
def counting_dumptruck(input_data, cycle_time_data, output_dir):
    df = pd.read_csv(input_data)
    df.rename(columns={'Unnamed: 0': 'time'}, inplace=True)

    act_time_df = pd.read_csv(cycle_time_data)
    act_time_df.drop(['Unnamed: 0', 'gap'], axis=1, inplace=True)
    act_time_list = act_time_df.values.tolist()
    checkpoint = []
    for act_time in act_time_list:
        if act_time[0] == 'Mucking':
            checkpoint.append(act_time)
    startpoint = checkpoint[0][1]
    endpoint = checkpoint[-1][2]

    df_act = df.loc[startpoint:endpoint]
    E1_list = df['dump_truck'].tolist()
    time_list = []
    semi_list = []
    length = len(E1_list)
    num_list = [0, 1]

    for num in num_list:
        semi_list = [num]
        for i in range(0, length):
            if E1_list[i] == num:
                if i == num:
                    semi_list.append(num)
                elif i == length - 1:
                    semi_list.append(i)
                    time_list.append(semi_list)
                    semi_list = [num]
                elif E1_list[i - 1] == num and E1_list[i + 1] == num:
                    continue
                elif E1_list[i - 1] == num and E1_list[i + 1] != num:
                    semi_list.append(i)
                    time_list.append(semi_list)
                    semi_list = [num]
                elif E1_list[i - 1] != num and E1_list[i + 1] == num:
                    semi_list.append(i)
                elif E1_list[i - 1] != num and E1_list[i + 1] != num:
                    continue

    count = 0
    for i in time_list:
        if i[0] == 1:
            count += 1

    #print('Dumptruck counting : ' + str(count))
    time_df = pd.DataFrame(time_list, columns=['ID', 'InTime', 'OutTime'])
    time_df.sort_values(by=['InTime'], axis=0, inplace=True)
    time_df.reset_index(drop=True, inplace=True)
    time_df.to_csv(output_dir+'/dumptruck_counting.csv')

def counting_payloader(input_data, dumptruck_counting_data, output_dir):
    df = pd.read_csv(input_data)
    df2 = df.replace(0, np.nan)
    dumptruck_time = pd.read_csv(dumptruck_counting_data)
    dumptruck_time = dumptruck_time[dumptruck_time.ID == 1]
    intime = dumptruck_time['InTime'].values.tolist()
    outtime = dumptruck_time['OutTime'].values.tolist()

    dumptruck_time_list = []
    for i in range(len(intime)):
        semi_list = []
        semi_list.append(intime[i])
        semi_list.append(outtime[i])
        dumptruck_time_list.append(semi_list)

    plt.figure(figsize=(20, 6))
    plt.title('Payloader', fontsize=30)
    plt.xlabel('Cycle Time')
    plt.ylabel('Coordinate')
    plt.rc('xtick', labelsize=10)
    plt.grid()
    plt.tight_layout()

    result = []
    for time in dumptruck_time_list:
        df3 = df2.iloc[time[0]:time[1], :]

        payloader = df3['payloader_cy']
        dumptruck = df3['dump_truck_cy']

        peaks, properties = find_peaks(payloader, height=450, distance=10)
        peak_list = list(time[0] + peaks)
        result.extend(peak_list)
        plt.plot(payloader, color='b')
        plt.plot(time[0] + peaks, payloader[time[0] + peaks], 'x', color='r')
        plt.plot(dumptruck, color='g')

    plt.savefig(output_dir+'/counting_payloader.jpg', facecolor='#eeeeee')
    time_df = pd.DataFrame(result, columns=['PeakTime'])
    time_df.to_csv(output_dir+'/payloader_counting.csv')


parser = argparse.ArgumentParser()
parser.add_argument('--mode', default = 'result_analysis', type=str, required=False)
parser.add_argument('--data', default = '../config/config.yaml', type=str, required=False,)
args = parser.parse_args()

#load yaml
myyaml = args.data
with open(myyaml)as f:
    Doc = yaml.load(f, Loader=yaml.FullLoader)
    doc = Doc["RESULT_ANALYSIS"]

#time_table
if args.mode == 'time_table':
    mode = 'time_table'
    input_ID_data= doc[mode]['input_ID_data']
    time_table_output_dir= doc[mode]['time_table_output_dir']
    time_interval=doc[mode]['time_interval']
    createFolder(time_table_output_dir)
    making_timetable(input_ID_data, time_table_output_dir, time_interval)

#activity_cylce_time
elif args.mode == 'activity_cycle_time':
    mode = 'activity_cycle_time'
    input_ID_data = doc[mode]['input_ID_data']
    cycle_time_output_dir = doc[mode]['cycle_time_output_dir']
    activity_class = doc[mode]['activity_class']
    createFolder(cycle_time_output_dir)
    time_of_activity(input_ID_data, cycle_time_output_dir, activity_class)

#counting_dumptruck
elif args.mode == 'counting_dumptruck':
    mode = 'counting_dumptruck'
    input_ID_data = doc[mode]['input_ID_data']
    cycle_time_data = doc[mode]['cycle_time_data']
    counting_output_dir = doc[mode]['counting_output_dir']
    createFolder(counting_output_dir)
    counting_dumptruck(input_ID_data, cycle_time_data, counting_output_dir)

#counting_payloader
elif args.mode == 'counting_payloader':
    mode = 'counting_payloader'
    input_XY_data = doc[mode]['input_XY_data']
    dumptruck_counting_data = doc[mode]['dumptruck_counting_data']
    counting_output_dir = doc[mode]['counting_output_dir']
    createFolder(counting_output_dir)
    counting_payloader(input_XY_data, dumptruck_counting_data, counting_output_dir)

elif args.mode == 'result_analysis':
    mode = 'result_analysis'
    input_ID_data = doc[mode]['input_ID_data']
    input_XY_data = doc[mode]['input_XY_data']
    time_table_output_dir = doc[mode]['time_table_output_dir']
    cycle_time_output_dir = doc[mode]['cycle_time_output_dir']
    counting_output_dir = doc[mode]['counting_output_dir']
    cycle_time_data = doc[mode]['cycle_time_data']
    dumptruck_counting_data = doc[mode]['dumptruck_counting_data']
    time_interval = doc[mode]['time_interval']
    activity_class = doc[mode]['activity_class']

    createFolder(time_table_output_dir)
    createFolder(cycle_time_output_dir)
    createFolder(counting_output_dir)

    making_timetable(input_ID_data, time_table_output_dir, time_interval)
    time_of_activity(input_ID_data, cycle_time_output_dir, activity_class)
    counting_dumptruck(input_ID_data, cycle_time_data, counting_output_dir)
    counting_payloader(input_XY_data, dumptruck_counting_data, counting_output_dir)
    print("result analysis finished!")