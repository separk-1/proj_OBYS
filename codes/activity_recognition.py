from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import os
import os.path as osp
import tensorflow as tf
from tensorflow.keras.models import Model,Sequential
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import LSTM, Dense, BatchNormalization, Dropout
from tensorflow.keras import regularizers
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.callbacks import EarlyStopping,Callback,ModelCheckpoint
from keras.models import load_model
from pandas import DataFrame
from sklearn.metrics import confusion_matrix, plot_confusion_matrix
from sklearn import metrics
from scipy import stats
import seaborn as sns
import argparse
import sys
sys.path.append("..")
import yaml


parser = argparse.ArgumentParser()

parser.add_argument("--mode", default = 'training', type=str, required=False,
                        help="Set the training mode. Do not forget to configure config.py accordingly !")
parser.add_argument("--data", default = "/home/obayashi/Projects/obayashi_practice/config/config.yaml", type=str, required=False,
                        help="Set the training mode. Do not forget to configure config.py accordingly !")                        
args = parser.parse_args()

#load yaml
myyaml = args.data
with open(myyaml)as f:
  Doc = yaml.load(f, Loader = yaml.FullLoader) 

#load csv file
def load_data_with_gt(df, columns, N_TIME_STEPS, num_equipment,step):
    N_TIME_STEPS = N_TIME_STEPS
    segments = []
    labels = []
    #step = round(N_TIME_STEPS/2)
    step = 1
    for i in range(1, len(df) - N_TIME_STEPS, step):
        List = []
        for j in range(1,len(columns)-1):
            List.append(df[columns[j]].values[i: i + N_TIME_STEPS])
                
        label = stats.mode(df['activity'][i: i + N_TIME_STEPS])[0][0]
        segments.append(List)
        labels.append(label)
    print("reduced size of data", np.array(segments).shape)
    reshaped_segments = np.asarray(segments,dtype=np.float32).reshape(-1, N_TIME_STEPS, N_FEATURES)
    labels = np.asarray(pd.get_dummies(labels),dtype=np.float32)
    print("Reshape the segments", np.array(reshaped_segments).shape)
        
    return labels, reshaped_segments
    
def load_data_without_gt(df, columns, N_TIME_STEPS, num_equipment,step):
    N_TIME_STEPS = N_TIME_STEPS
    segments = []
    step = 1  #round(N_TIME_STEPS/2)
    for i in range(1, len(df) - N_TIME_STEPS, step):
        List = []
        for j in range(1,len(columns)):
            List.append(df[columns[j]].values[i: i + N_TIME_STEPS])
                
        segments.append(List)
    print("reduced size of data", np.array(segments).shape)
    reshaped_segments = np.asarray(segments,dtype=np.float32).reshape(-1, N_TIME_STEPS, N_FEATURES)
    print("Reshape the segments", np.array(reshaped_segments).shape)
    return reshaped_segments

def create_model(N_TIME_STEPS,N_FEATURES,optimizer): #SGD()
        model = Sequential([
           Dense(n_hidden, activation='relu'
           ),
           BatchNormalization(), 
           LSTM(n_hidden, input_shape = (N_TIME_STEPS,N_FEATURES), return_sequences=True,  unit_forget_bias=1.0,dropout=0.2),
           LSTM(n_hidden,  unit_forget_bias=1.0),
           Dropout(0.5),
           Dense(n_classes,
               activation='softmax'
           )
        ]) 
    
        #LR range test 
        model.compile(
           optimizer=optimizer,
           metrics=['accuracy'],
           loss='categorical_crossentropy'
        )
        return model
        
#set mode
if args.mode =='training':
    doc = Doc['ACTIVITY_RECOGNITION']
    train_dir = doc['train']['input_dir']
    N_TIME_STEPS = int(doc['train']['N_TIME_STEPS'])
    step = int(doc['train']['step'])
    num_equipment = int(doc['train']['num_equipment'])
    N_FEATURES = 2*num_equipment
    n_classes = int(doc['train']['n_classes'])
    res_dir = doc['train']['res_dir']
    epoch = doc['train']['epoch']
    n_hidden = doc['train']['n_hidden']
    batch_size = doc['train']['batch_size']
    
    
    #call yaml-based variable
    RANDOM_SEED = 42
    columns =['time']
    for equip in range(num_equipment):
        columns.append('e{}x'.format(str(equip+1)))
        columns.append('e{}y'.format(str(equip+1)))
    columns.append('activity')
    #####input####
    df = pd.read_csv(train_dir, header = None, names = columns)
    labels, reshaped_segments = load_data_with_gt(df, columns,N_TIME_STEPS, num_equipment,step)
    ###GPU memory growth control
    gpus = tf.config.list_physical_devices('GPU')
    for i in range(len(gpus)):
	     tf.config.experimental.set_memory_growth(gpus[i], True)
        
    X_train, X_test, y_train, y_test = train_test_split(reshaped_segments, labels, test_size=0.3, shuffle=True,random_state=RANDOM_SEED)
    print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
        
    training_data_count = len(X_train)  
    test_data_count = len(X_test)  
    n_input = len(X_train[0][0])
        
    y_train_one_hot = to_categorical(y_train, num_classes=6)
    y_test_one_hot = to_categorical(y_test, 6)
        
    train_size = X_train.shape[0] - X_train.shape[0] % batch_size
    test_size = X_test.shape[0] - X_test.shape[0] % batch_size
    
    optimizer = SGD()
    model = create_model(N_TIME_STEPS,N_FEATURES,optimizer)
    checkpoint_path = "{}/cp.ckpt".format(res_dir)
    checkpoint_dir = os.path.dirname(checkpoint_path)
    cp_callback = ModelCheckpoint(filepath=checkpoint_path,
                                                         save_weights_only=True,
                                                         verbose=1) #callback where weights are saved
                
    history = model.fit(
            X_train, y_train, validation_data=(X_test, y_test), batch_size=batch_size, epochs=epoch, callbacks = [cp_callback]
        )                            
    ###output_file_name as h5 format ### 
    model.save('{}/lstm_epoch{}_timestep{}.h5'.format(res_dir,epoch, N_TIME_STEPS))
            
#set mode
if args.mode =='predicting':
    doc = Doc['ACTIVITY_RECOGNITION']
    N_TIME_STEPS = int(doc['predict']['N_TIME_STEPS'])
    step = int(doc['predict']['step'])
    num_equipment = int(doc['predict']['num_equipment'])
    N_FEATURES = 2*num_equipment
    n_classes = int(doc['predict']['n_classes'])
    res_dir = doc['predict']['res_dir']
    input_file = doc['predict']['input_file']
    input_file_name = input_file.split('/')[-1]
    trained_model = doc['predict']['trained_model']
    
    N_FEATURES = 2*num_equipment
    
    RANDOM_SEED = 42
    
    model = load_model(trained_model)
    columns =['time']
    for equip in range(num_equipment):
        columns.append('e{}x'.format(str(equip+1)))
        columns.append('e{}y'.format(str(equip+1)))
    df = pd.read_csv(input_file, skiprows = [0], names = columns,index_col='time')
    X_test = load_data_without_gt(df, columns, N_TIME_STEPS, num_equipment,step)
    
    #output_1: comparison_table 
    yhat = model.predict(X_test, verbose=0, batch_size=32)
    Predict_class = []
    yhat = yhat.tolist()
    for i in yhat:
        pred_class_index = i.index(max(i))
        label_list = ['A','B','C','D','E','F','I']
        Predict_class.append(label_list[pred_class_index]) #predict_class
    print(columns)
    
    Dict = {}
    df_for_name = pd.read_csv(input_file)  #for getting the column name
    new_column = []
    for col in df_for_name.columns:
        new_column.append(col)
    print(new_column)
    for i in range(len(columns)):
        Dict[columns[i]] = new_column[i]
    
    
    df = pd.read_csv(input_file, skiprows = [0], names = columns)
    df.drop(df.columns[[0]], axis=1, inplace=True)
    last_class = Predict_class[-1]
    i = 0
    for i in range(N_TIME_STEPS+1):
        Predict_class.append(last_class)
        i +=1    
    df['predict_class'] = Predict_class
    res_file_xy = res_dir + '/' + '{}'.format(input_file_name)
    df.rename(columns = Dict, inplace=True)
    df.to_csv(res_file_xy)
    
    ###read ID file ###
    input_file_name_ID = input_file_name.replace('xy_mod','ID')
    input_ID_file = input_file.replace('xy_mod','ID')
    #print(input_ID_file)
    df_ID = pd.read_csv(input_ID_file, index_col=0)
    print(len(Predict_class))
    df_ID['predict_class'] = Predict_class
    res_file_ID = res_dir + '/' + '{}'.format(input_file_name_ID)
    df_ID.to_csv(res_file_ID)
        


if args.mode =='comparison':
    ###input_csv file you want to predict _ with only coordinates information and groundtruth activity###
    doc = Doc['ACTIVITY_RECOGNITION']
    N_TIME_STEPS = int(doc['comparison']['N_TIME_STEPS'])
    step = int(doc['comparison']['step'])
    num_equipment = int(doc['comparison']['num_equipment'])
    N_FEATURES = 2*num_equipment
    n_classes = int(doc['comparison']['n_classes'])
    res_dir = doc['comparison']['res_dir']
    input_file = doc['comparison']['input_file']
    trained_model = doc['comparison']['trained_model']

    RANDOM_SEED = 42
    columns =['time']
    for equip in range(num_equipment):
        columns.append('e{}x'.format(str(equip+1)))
        columns.append('e{}y'.format(str(equip+1)))
    columns.append('activity')
    df = pd.read_csv(input_file, header = None, names = columns)
    
    model = load_model(trained_model)
    labels, reshaped_segments = load_data_with_gt(df, columns, N_TIME_STEPS, num_equipment,step)
        
    X_test = reshaped_segments
    y_test = labels
        
    #output_2: confusion matrix            
    yhat = model.predict(X_test, verbose=0, batch_size=32)
    predict_class = []
    yhat = yhat.tolist()
    for i in yhat:
        pred_class_index = i.index(max(i))
        predict_class.append(pred_class_index) #predict_class
        
    YY_test = []
    for ij in y_test:
        Test = np.argmax(ij)
        YY_test.append(Test) #Y_test
           
    label=[i for i in range(n_classes)]  
    a = metrics.confusion_matrix(YY_test, predict_class, labels=label)
    labels = ['Drilling','Mucking','Scaling', 'Spraying','H_beam','Rock_bolting','Resting']
    df_cm = DataFrame(a,index=[i for i in labels],
                  columns = [i for i in labels])
    plt.figure(figsize=(10,7))
    plt.title('Result_time_step_{}'.format(N_TIME_STEPS))
    sns.heatmap(df_cm,annot=True,fmt='g')
    ###output_png_filepath###
    plt.savefig('{}/Result_time_step_{}.jpg'.format(res_dir, N_TIME_STEPS))    #confusion matrix image will be saved in your res path
    
