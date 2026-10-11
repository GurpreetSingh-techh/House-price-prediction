from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import os
from huggingface_hub import hf_hub_download

app = Flask(__name__)


# ==========================================
# LOAD MACHINE LEARNING MODEL
# ==========================================

# Download the model from Hugging Face
model_path = hf_hub_download(
    repo_id="GurpreetSingh21/house-price-model",
    filename="house_price_model.pkl"
)

# Load the trained model
model = joblib.load(model_path)


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# PREDICTION
# ==========================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # Get values from HTML form

        overall_qual = float(request.form["overall_qual"])
        gr_liv_area = float(request.form["gr_liv_area"])
        garage_cars = float(request.form["garage_cars"])
        total_bsmt_sf = float(request.form["total_bsmt_sf"])
        first_flr_sf = float(request.form["first_flr_sf"])
        year_built = float(request.form["year_built"])
        full_bath = float(request.form["full_bath"])
        bedroom_abvgr = float(request.form["bedroom_abvgr"])
        garage_area = float(request.form["garage_area"])
        lot_area = float(request.form["lot_area"])

        # Create DataFrame

        house = pd.DataFrame({

            "Overall Qual": [overall_qual],
            "Gr Liv Area": [gr_liv_area],
            "Garage Cars": [garage_cars],
            "Total Bsmt SF": [total_bsmt_sf],
            "1st Flr SF": [first_flr_sf],
            "Year Built": [year_built],
            "Full Bath": [full_bath],
            "Bedroom AbvGr": [bedroom_abvgr],
            "Garage Area": [garage_area],
            "Lot Area": [lot_area]

        })

        # Make prediction

        prediction = model.predict(house)[0]

        # Return result

        return jsonify({
            "success": True,
            "price": round(float(prediction), 2)
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


# ==========================================
# RUN FLASK
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)

