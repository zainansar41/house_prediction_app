from flask import Flask, request, jsonify
from flask_cors import CORS
import util
import numpy as np

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

        property_mapping = {
            "Apartment": 0,
            "House": 1,
            "Penthouse": 2,
            "Farm House": 3,
            "Lower Portion": 4,
            "Upper Portion": 5,
            "Room": 6,
        }
        city_mapping = {
            "Islamabad": 0,
            "Lahore": 1,
            "Faisalabad": 2,
            "Rawalpindi": 3,
            "Karachi": 4,
        }

        selectedPropertyType = property_mapping.get(data.get("propertyType"), None)
        selectedCity = city_mapping.get(data.get("city"), None)
        adjustedHouseSize = data.get("houseSize")
        numberOfBedrooms = data.get("numberOfBedrooms")
        selectedLocation = data.get("location")

        # Get predictions from both models
        predicted_price_linear_reg = util.get_estimated_price(
            selectedLocation,
            numberOfBedrooms,
            adjustedHouseSize,
            selectedPropertyType,
            selectedCity,
        )
        predicted_price_ann = util.predict_price_ann(
            selectedLocation,
            numberOfBedrooms,
            adjustedHouseSize,
            selectedPropertyType,
            selectedCity,
        )

        predicted_price_linear_reg = (
            predicted_price_linear_reg.item()
            if predicted_price_linear_reg is not None
            else None
        )
        predicted_price_ann = (
            predicted_price_ann.item() if predicted_price_ann is not None else None
        )

        print("getting request")
        return jsonify(
            {
                "predicted_price_linear_reg": predicted_price_linear_reg,
                "predicted_price_ann": predicted_price_ann,
            }
        )

    except Exception as e:
        # Handle any exceptions that may occur during the prediction
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    util.load_saved_artifacts()

    # Example usage for linear regression
    print(
        "Linear Regression Model Prediction:",
        int(util.get_estimated_price("others", 3, 0.5, 1, 4)),
    )

    # Example usage for ANN
    print("ANN Model Prediction:", int(util.predict_price_ann("others", 3, 0.5, 1, 4)))

    app.run(port=4000)
