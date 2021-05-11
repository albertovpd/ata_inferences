import json
import pandas as pd
from functions import haversine_distance, redo_1hot_encoder, str_to_int

import pickle # trained model
from sklearn.preprocessing import StandardScaler 
from sklearn.linear_model import LinearRegression


def ata_fir_function(data):
    '''Calculates the ata once the flight enters the fir'''
    
    # add to the input dictionary distance from airports
    df_coords= pd.DataFrame(data, index=[0]) #because of recycling from jupyter 
    data["km_from_departure"]=haversine_distance(
        df_coords, ['adep_latitude','adep_longitude']).values[0] 

    # transform str dates into numerical
    #df = str_to_int(data, [column_list_of_features])

    # match the input json with our template
    df = redo_1hot_encoder(data) 

    # bringing trained fit for our X
    pkl_filename = "output/trained_scaler.pkl"
    with open(pkl_filename, 'rb') as file:
        pickle_scaler = pickle.load(file)
    x_test=pickle_scaler.transform(df)

    # trained model
    pkl_filename = "output/trained_model.pkl"
    with open(pkl_filename, 'rb') as file:
        pickle_model = pickle.load(file)
    ypredict = pickle_model.predict(x_test)

    return str(pd.to_datetime(ypredict*10**9))[16:35]
