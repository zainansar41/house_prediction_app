from flask import Flask, request, jsonify
from flask_cors import CORS 
import util


app = Flask(__name__)
CORS(app)  


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/toPredictPrice", methods=["POST"])
def predict_price():
    try:
        data = request.json
        print(data)

        property_mapping = {"Apartment": 0, "House": 1, "Penthouse": 2, "Farm House": 3, "Lower Portion": 4, "Upper Portion": 5, "Room": 6}
        city_mapping = {"Islamabad": 0, "Lahore": 1, "Faisalabad": 2, "Rawalpindi": 3, "Karachi": 4}

        selectedPropertyType = property_mapping.get(data.get("propertyType"), None)
        selectedCity = city_mapping.get(data.get("city"), None)
        adjustedHouseSize = data.get("houseSize")
        numberOfBedrooms = data.get("numberOfBedrooms")
        selectedLocation = data.get("location")
        predicted_price = util.get_estimated_price(selectedLocation,numberOfBedrooms,adjustedHouseSize,selectedPropertyType,selectedCity)

        print("getting request")
        return jsonify({"predicted_price": predicted_price})

    except Exception as e:
        # Handle any exceptions that may occur during the prediction
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    util.load_saved_artifacts()
    print(int(util.get_estimated_price('others',3,.5,1,4)))
    app.run(port=4000)
