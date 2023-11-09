from flask import Flask, request, jsonify
from flask_cors import CORS  
app = Flask(__name__)
CORS(app)  


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/toPredictPrice", methods=["POST"])
def predict_price():
    try:
        data = request.json

        selectedCity = data.get("city")
        selectedPropertyType = data.get("propertyType")
        adjustedHouseSize = data.get("houseSize")
        numberOfBedrooms = data.get("numberOfBedrooms")
        selectedLocation = data.get("location")
        predicted_price = 100000

        # Return the predicted price as JSON
        print("Predicted price: ", predicted_price)
        return jsonify({"predicted_price": predicted_price})

    except Exception as e:
        # Handle any exceptions that may occur during the prediction
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(port=4000)
