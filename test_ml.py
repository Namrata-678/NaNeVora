from ml_engine.predict import predict_loan


test_data = {

    "no_of_dependents": 2,

    "education": "Graduate",

    "self_employed": "No",

    "income_annum": 600000,

    "loan_amount": 2000000,

    "loan_term": 10,

    "cibil_score": 750,

    "residential_assets_value": 3000000,

    "commercial_assets_value": 1000000,

    "luxury_assets_value": 500000,

    "bank_asset_value": 1000000,
}


result = predict_loan(test_data)


print("\n==============================")
print("      NaNeVora ML TEST")
print("==============================")

print("Prediction :", result["prediction"])

print(
    "Confidence :",
    result["confidence"]
)

print(
    "Loan/Income Ratio :",
    result["loan_income_ratio"]
)

print(
    "Total Assets :",
    result["total_assets"]
)

print(
    "Asset/Loan Ratio :",
    result["asset_loan_ratio"]
)

print("==============================")