import os
import joblib
import pandas as pd


# ==========================================================
# MODEL PATHS
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")


# ==========================================================
# LOAD TRAINED MODEL AND ENCODERS
# ==========================================================

model = joblib.load(
    os.path.join(MODEL_DIR, "loan_approval_model.pkl")
)

education_encoder = joblib.load(
    os.path.join(MODEL_DIR, "education_encoder.pkl")
)

self_employed_encoder = joblib.load(
    os.path.join(MODEL_DIR, "self_employed_encoder.pkl")
)

loan_status_encoder = joblib.load(
    os.path.join(MODEL_DIR, "loan_status_encoder.pkl")
)


# ==========================================================
# PREDICTION FUNCTION
# ==========================================================

def predict_loan(data):

    # ------------------------------------------------------
    # Encode categorical values
    # ------------------------------------------------------

    education = education_encoder.transform(
        [data["education"]]
    )[0]

    self_employed = self_employed_encoder.transform(
        [data["self_employed"]]
    )[0]


    # ------------------------------------------------------
    # Prepare input data
    # ------------------------------------------------------

    loan_amount = float(data["loan_amount"])
    income_annum = float(data["income_annum"])

    residential_assets = float(
        data["residential_assets_value"]
    )

    commercial_assets = float(
        data["commercial_assets_value"]
    )

    luxury_assets = float(
        data["luxury_assets_value"]
    )

    bank_assets = float(
        data["bank_asset_value"]
    )


    # ------------------------------------------------------
    # Feature Engineering
    # ------------------------------------------------------

    loan_income_ratio = (
        loan_amount / income_annum
        if income_annum != 0
        else 0
    )

    total_assets = (
        residential_assets
        + commercial_assets
        + luxury_assets
        + bank_assets
    )

    asset_loan_ratio = (
        total_assets / loan_amount
        if loan_amount != 0
        else 0
    )


    # ------------------------------------------------------
    # Create DataFrame
    # ------------------------------------------------------

    input_data = {
        "no_of_dependents": [
            int(data["no_of_dependents"])
        ],

        "education": [education],

        "self_employed": [self_employed],

        "income_annum": [income_annum],

        "loan_amount": [loan_amount],

        "loan_term": [
            float(data["loan_term"])
        ],

        "cibil_score": [
            float(data["cibil_score"])
        ],

        "residential_assets_value": [
            residential_assets
        ],

        "commercial_assets_value": [
            commercial_assets
        ],

        "luxury_assets_value": [
            luxury_assets
        ],

        "bank_asset_value": [
            bank_assets
        ],

        "loan_income_ratio": [
            loan_income_ratio
        ],

        "total_assets": [
            total_assets
        ],

        "asset_loan_ratio": [
            asset_loan_ratio
        ],
    }


    df = pd.DataFrame(input_data)


    # ------------------------------------------------------
    # Make Prediction
    # ------------------------------------------------------

    prediction = model.predict(df)[0]


    # ------------------------------------------------------
    # Convert Prediction
    # ------------------------------------------------------

    result = loan_status_encoder.inverse_transform(
        [prediction]
    )[0].strip()


    # ------------------------------------------------------
    # Prediction Probability
    # ------------------------------------------------------

    confidence = None

    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(df)[0]

        confidence = float(max(probabilities) * 100)


    # ------------------------------------------------------
    # Return Results
    # ------------------------------------------------------

    return {
        "prediction": result,
        "confidence": confidence,
        "loan_income_ratio": loan_income_ratio,
        "total_assets": total_assets,
        "asset_loan_ratio": asset_loan_ratio,
    }