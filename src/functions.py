import json

import numpy as np
import math
import pandas as pd

def redo_1hot_encoder(data):
    '''
    Analysing the project, I transformed categorical columns into numericals with 1-hot encoder.
    Now, I  have to transform the incoming data to match the created columns.
    - template == this is the shape of my X set.
    - data == the input json file. For further info about input data check the Readme.
    '''
    with open('json_folder/data_template.json') as json_file:
        template = json.load(json_file)
    
    for d in data:
        if d in template:
            template[d]=data[d]

        elif d=="skyc1_okt":
            if data[d]=='BKN':
                template['meteo_BKN']=1
            elif data[d]=='FEW':
                template['meteo_FEW']=1
            elif data[d]=='NCD':
                template['meteo_NCD']=1
            elif data[d]=='NSC':
                template["meteo_NSC"]=1
            elif data[d]=='OVC':
                template["meteo_OVC"]=1
            elif data[d]=="SCT":
                template['meteo_SCT']=1
            elif data[d]=='VV ':
                template['meteo_VV ']=1
            else: 
                template['meteo_unknown']=1

        elif d=="market_segment":
            if data[d]=='Traditional Scheduled':
                template['Traditional Scheduled']=1
            elif data[d]=='Lowcost':
                template['Lowcost']=1
            elif data[d]=='Charter':
                template['Charter']=1
            elif data[d]=='Business Aviation':
                template['Business Aviation']=1
            else:
                template['All-Cargo']=1

        elif d=="icao_flight_type":
            if data[d]=='S':
                template['S']=1
            elif data[d]=='N':
                template['N']=1
    
    return pd.DataFrame(template, index=[0])


def haversine_distance(df, coordinates):
    '''
    - This function calculates the haversine distance (taking into account the curvature of Earth) from the starting airport 
    to our chosen one.
    - Delivers an array to create a new column in the df.
    - Removes the coordinates columns from df.
    
    coordinates : list == [latitude, longitude]
    '''
    london_lat  = 51.4775 	
    london_long = -0.46139
    
    airport_lat= df[coordinates[0]]
    airport_long= df[coordinates[1]]
    df.drop(columns=coordinates,inplace=True)
    
    return round(6372.8 * 2 * np.arcsin( # pure haversine eq with Earth radious in km
        np.sqrt(
                np.sin((np.radians(airport_lat) - math.radians(london_long ))/2)**2 
                + math.cos(math.radians(london_long)) * np.cos(np.radians(airport_lat)) * np.sin((np.radians(airport_long) - math.radians(london_lat))/2)**2
                )),0)


def categorical_numerical(df):
    '''
    Transforming all categorical data of a dataframe into numerical.
    c == column of dataset
    k == keywords of the column c
    '''
    for c in df.columns:
        if df[c].dtypes == object:
            for k in df[c].unique():
                df[k]=df[c].apply(lambda x: 1 if x==k else 0)
            
            # don't mix up identation with this
            df.drop(columns=[c],inplace=True) 
    return df

def str_to_int(df,column_list):
    '''
    For transforming the json dates
    '''
    for c in column_list:
        dates=pd.to_datetime(df[c], format='%Y-%m-%d %H:%M:%S.%f')
        df[c]= (dates- pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
    return df

def datetime_to_int(df):
    '''
    Changing type of date columns to have workable columns with the ML model
    
    # just checking how to return t its state
    #pd.to_datetime(df_flights.actual_arrival_time)
    Pandas docs recommend using the following method
    '''
    for c in df.columns:
        #if df[c].dtypes == "timedelta64[ns]":
        #    df[c]=df[c].values.astype('datetime64[D]')
            
        if df[c].dtypes == '<M8[ns]' : # datetime dtype
            
            dates = pd.to_datetime(df[c])
            df[c]= (dates- pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
    return df
