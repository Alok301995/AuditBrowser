import pandas as pd
import numpy as np
import tensorflow as tf
from keras.models import load_model

################################################################################

window_size = 200 #Length of time slice. Actitrac was recorded at 20Hz
start = 0
end = 200
act = {1:"Jogging" ,5:"Walking" ,2:"Sitting" ,0:"Downstairs" ,4:"Upstairs" ,3:"Standing"}
act_1 = {"Jogging":1 ,"Walking":5 ,"Sitting":2 ,"Downstairs":0 ,"Upstairs":4 ,"Standing":3}

################################################################################

def convert_data(data):
    acc =[]
    if len(data) != 0 and len(data) > 200:
        for i in data:
            i[0] , i[1] ,i[2] = float(i[0]) , float(i[1]) , float(i[2])
            acc.append(i)
    return acc

################################################################################

def create_df(data):
    df = pd.DataFrame(data , columns=['x-axis','y-axis','z-axis'])
    return df

################################################################################

def read_input(file_path):
    column_names = ['user-id','activity','timestamp', 'x-axis', 'y-axis', 'z-axis' ,'target']
    data = pd.read_csv(file_path,header = None, names = column_names)
    return data

################################################################################

def find_activity(activity):
    return act[activity]

################################################################################

def feature_normalize(dataset):
    mu = np.mean(dataset,axis = 0)
    sigma = np.std(dataset,axis = 0)
    return (dataset - mu)/sigma

################################################################################

def windows(data, size):
    start = 0
    while start < data.count():
        yield int(start), int(start + size)
        start += (size / 2)
        
################################################################################ 
       
def segment_signal(data,window_size):
    segments = np.empty((0,window_size,3))
    labels = np.empty((0))
    for (start, end) in windows(data["x-axis"], window_size):
        x = data["x-axis"][start:end]
        y = data["y-axis"][start:end]
        z = data["z-axis"][start:end]
        if(len(data["x-axis"][start:end]) == window_size):
            segments = np.vstack([segments,np.dstack([x,y,z])])
            # labels = np.append(labels,stats.mode(data["activity"][start:end])[0][0])
    return segments

################################################################################

def detect_activity(df):
    df['x-axis'] = feature_normalize(df['x-axis'])
    df['y-axis'] = feature_normalize(df['y-axis'])
    df['z-axis'] = feature_normalize(df['z-axis'])
    # Segmenting Data
    segments  = segment_signal(df ,window_size)
    # Reshaping Segments
    segments = segments.reshape(len(segments) ,200 ,3)
    
    # new_label = []
    # for i in label:
    #     new_label.append(act_1[i])
    # new_label = np.array(new_label)
    
    # Load the best_model file from folder model
    model = load_model('./src/services/lstm_model.h5')
    # Prediction
    pred = np.argmax(model.predict(segments) , axis= 1)
    
    # Most frequent Predition label
    frq = np.bincount(pred).argmax()
    pred_activity = find_activity(frq)
    
    return pred_activity

################################################################################

if __name__ =='__main__':
    pass

################################################################################