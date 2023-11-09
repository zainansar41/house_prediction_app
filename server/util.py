import pickle
import json
import numpy as np
import warnings



__locations = None
__data_columns = None
__model = None

def get_estimated_price(location, numberOfBedrooms, houseSize, propertyType, city):
    try:
        loc_index = __data_columns.index(location.lower())
        print(loc_index)
    except ValueError:
        loc_index = -1
        print("Location not found in data columns")

    x = np.zeros(len(__data_columns))
    x[0] = propertyType
    x[1] = city
    x[2] = houseSize
    x[3] = numberOfBedrooms

    if loc_index >= 0:
        x[loc_index] = 1

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            predicted = __model.predict([x])[0]
            print(predicted)
            return predicted
    except Exception as e:
        print(f"Error predicting price: {e}")
        return None



def load_saved_artifacts():
    print("loading saved artifacts...start")
    global  __data_columns
    global __locations

    with open("D:\\Github\\house_prediction_app\\server\\helper\\columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[4:]  
        print(__locations)

    global __model
    if __model is None:
        with open('D:\\Github\\house_prediction_app\\server\\helper\\zameen_price_model.pickle', 'rb') as f:
            __model = pickle.load(f)
    print("loading saved artifacts...done")

def get_location_names():
    return __locations

def get_data_columns():
    return __data_columns