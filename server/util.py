import pickle
import json
import numpy as np
import warnings
from tensorflow.keras.models import load_model  # Add this import
# from sklearn.preprocessing import StandardScaler

__locations = None
__data_columns = None
__model = None
__model_ann = None
# scaler = StandardScaler()


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
            return abs(predicted)
    except Exception as e:
        print(f"Error predicting price: {e}")
        return None


import json
import numpy as np

__model_ann = None
__scaler = None
__data_columns = []


def predict_price_ann(location, numberOfBedrooms, houseSize, propertyType, city):
    try:
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        # If the location is not in the columns, set the loc_index to 0 (or handle it as needed)
        loc_index = 0

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

            x_scaled = __scaler.transform([x])

            predicted = __model_ann.predict(x_scaled)[0][0]
            print(predicted)
            return abs(predicted)
    except Exception as e:
        print(f"Error predicting price: {e}")
    # Return a default value (e.g., 0) in case of an exception
        return 0



def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __data_columns
    global __locations
    global __model_ann

    try:
        with open(
            "D:/Github/house_prediction_app/server/helper/columns.json",
            "r",
        ) as f:
            data = json.load(f)
            __data_columns = data.get("data_columns", [])
            __locations = __data_columns[4:]
            print(__locations)
    except Exception as e:
        print(f"Error loading columns.json: {e}")
        __data_columns = []
        __locations = []

    global __model
    if __model is None:
        with open(
            "D:/Github/house_prediction_app/server/helper/zameen_price_model.pickle",
            "rb",
        ) as f:
            __model = pickle.load(f)

    global __model_ann
    global __scaler
    if __model_ann is None or scaler is None:
        with open(
            "D:/Github/house_prediction_app/server/helper/zameen_price_model_and_scaler_ann.pickle",
            "rb",
        ) as f1:
            model_and_scaler_data = pickle.load(f1)
            __model_ann = model_and_scaler_data['model']
            __scaler = model_and_scaler_data['scaler']

    print("loading saved artifacts...done")


def get_location_names():
    return __locations


def get_data_columns():
    return __data_columns
