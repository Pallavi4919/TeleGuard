from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
import shap
import json
import io
from collections import Counter

# =====================================================
# Load Model
# =====================================================

model = joblib.load("../models/churn_model.pkl")
scaler = joblib.load("../models/scaler.pkl")

with open("../models/feature_columns.json", "r") as f:
    feature_columns = json.load(f)

explainer = shap.TreeExplainer(model)

# =====================================================
# Feature Explanations
# =====================================================

FEATURE_EXPLANATIONS = {

    "Contract_Month-to-month": {
        "title": "Flexible Contract Plans",
        "reason": "Customers on Month-to-Month contracts have a higher tendency to switch providers because they are not committed to a long-term plan.",
        "recommendation": "Offer discounts or loyalty benefits to encourage annual plans."
    },

    "InternetService_Fiber optic": {
        "title": "Premium Internet Plans",
        "reason": "Customers using Fiber Optic services are leaving more frequently, suggesting dissatisfaction with pricing or perceived value.",
        "recommendation": "Review pricing and improve service quality."
    },

    "PaymentMethod_Electronic check": {
        "title": "Manual Payment Method",
        "reason": "Customers using Electronic Check are more likely to churn than customers using automatic payments.",
        "recommendation": "Encourage customers to enroll in AutoPay."
    },

    "tenure": {
        "title": "New Customer Risk",
        "reason": "Recently joined customers have not yet developed long-term loyalty.",
        "recommendation": "Strengthen onboarding and early engagement."
    },

    "MonthlyCharges": {
        "title": "High Monthly Charges",
        "reason": "Customers with high monthly charges are more price-sensitive.",
        "recommendation": "Provide personalized pricing offers."
    },

    "TechSupport_No": {
        "title": "No Tech Support",
        "reason": "Customers without technical support tend to leave more often.",
        "recommendation": "Promote Tech Support plans."
    },

    "OnlineSecurity_No": {
        "title": "No Online Security",
        "reason": "Customers without Online Security are more likely to churn.",
        "recommendation": "Bundle security services into retention offers."
    },

    "Contract_One year": {
        "title": "Annual Contract Protection",
        "reason": "Customers without an annual commitment can switch providers more easily.",
        "recommendation": "Promote one-year contracts."
    },

    "Contract_Two year": {
        "title": "Long-Term Contract Protection",
        "reason": "Long-term contracts significantly reduce churn.",
        "recommendation": "Offer incentives for two-year plans."
    }

}

# =====================================================
# Business Strategies
# =====================================================

BUSINESS_STRATEGIES = {

    "Flexible Contract Plans": {
        "strategy": "Increase Long-Term Contract Adoption",
        "actions": [
            "Offer annual contract discounts.",
            "Launch loyalty reward campaigns.",
            "Target Month-to-Month customers."
        ],
        "impact": "High"
    },

    "Premium Internet Plans": {
        "strategy": "Improve Premium Internet Experience",
        "actions": [
            "Review Fiber pricing.",
            "Improve network quality.",
            "Provide proactive customer support."
        ],
        "impact": "High"
    },

    "Manual Payment Method": {
        "strategy": "Increase AutoPay Adoption",
        "actions": [
            "Promote AutoPay.",
            "Offer cashback.",
            "Simplify payment setup."
        ],
        "impact": "Medium"
    },

    "New Customer Risk": {
        "strategy": "Improve Customer Onboarding",
        "actions": [
            "Provide welcome offers.",
            "Contact customers during first 90 days.",
            "Increase engagement."
        ],
        "impact": "Medium"
    },

    "High Monthly Charges": {
        "strategy": "Reduce Pricing Concerns",
        "actions": [
            "Offer personalized discounts.",
            "Recommend better plans.",
            "Reward loyal customers."
        ],
        "impact": "Medium"
    },

    "No Tech Support": {
        "strategy": "Increase Tech Support Adoption",
        "actions": [
            "Offer free trials.",
            "Promote Tech Support plans.",
            "Resolve customer issues faster."
        ],
        "impact": "Medium"
    },

    "No Online Security": {
        "strategy": "Promote Security Services",
        "actions": [
            "Bundle Online Security.",
            "Offer discounts.",
            "Educate customers."
        ],
        "impact": "Medium"
    },

    "Annual Contract Protection": {
        "strategy": "Increase One-Year Contracts",
        "actions": [
            "Offer annual discounts.",
            "Provide exclusive benefits.",
            "Run renewal campaigns."
        ],
        "impact": "High"
    },

    "Long-Term Contract Protection": {
        "strategy": "Increase Two-Year Contracts",
        "actions": [
            "Provide premium benefits.",
            "Offer contract renewal rewards.",
            "Launch targeted campaigns."
        ],
        "impact": "High"
    }

}

# =====================================================
# Helper Functions
# =====================================================

def translate_feature(feature):

    if feature in FEATURE_EXPLANATIONS:
        return FEATURE_EXPLANATIONS[feature]

    return {
        "title": feature.replace("_", " "),
        "reason": f"{feature} contributed to the churn prediction.",
        "recommendation": "Review this feature."
    }


def get_business_strategy(driver):

    title = driver["title"]

    strategy = BUSINESS_STRATEGIES.get(title)

    if strategy is None:

        strategy = {
            "strategy": "Improve Customer Retention",
            "actions": [
                "Review customer behaviour.",
                "Create targeted campaigns.",
                "Improve customer satisfaction."
            ],
            "impact": "Medium"
        }

    return {

        "strategy": strategy["strategy"],

        "why": driver["reason"],

        "covers_customers": driver["affected_customers"],

        "coverage_percentage": driver["percentage"],

        "business_action": strategy["actions"],

        "priority": strategy["impact"]

    }

# =====================================================
# FastAPI App
# =====================================================

app = FastAPI(
    title="TeleGuard AI API",
    description="Customer Churn Prediction & Business Intelligence API",
    version="2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# Input Schema
# =====================================================

class CustomerData(BaseModel):

    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


REQUIRED_COLUMNS = list(CustomerData.model_fields.keys())

# =====================================================
# Preprocessing Functions
# =====================================================

def preprocess_input(data: CustomerData):

    df = pd.DataFrame([data.model_dump()])

    return encode_and_scale(df)


def preprocess_dataframe(df):

    return encode_and_scale(df.copy())


def encode_and_scale(df):

    # -------------------------------
    # Clean TotalCharges
    # -------------------------------

    df["TotalCharges"] = pd.to_numeric(
        df["TotalCharges"],
        errors="coerce"
    )

    df["TotalCharges"] = df["TotalCharges"].fillna(0)

    # -------------------------------
    # Binary Encoding
    # -------------------------------

    binary_map = {
        "Yes": 1,
        "No": 0
    }

    for col in [

        "Partner",
        "Dependents",
        "PhoneService",
        "PaperlessBilling"

    ]:

        df[col] = df[col].map(binary_map)

    # Gender Encoding

    df["gender"] = df["gender"].map({

        "Male": 1,
        "Female": 0

    })

    # -------------------------------
    # One-Hot Encoding
    # -------------------------------

    categorical_columns = [

        "MultipleLines",
        "InternetService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
        "Contract",
        "PaymentMethod"

    ]

    df = pd.get_dummies(
        df,
        columns=categorical_columns
    )

    # -------------------------------
    # Match Training Features
    # -------------------------------

    df = df.reindex(
        columns=feature_columns,
        fill_value=0
    )

    # -------------------------------
    # Scale Numerical Features
    # -------------------------------

    numeric_columns = [

        "tenure",
        "MonthlyCharges",
        "TotalCharges"

    ]

    df[numeric_columns] = scaler.transform(
        df[numeric_columns]
    )

    return df


# =====================================================
# Risk Level
# =====================================================

def get_risk_level(probability):

    if probability >= 0.60:
        return "High"

    elif probability >= 0.30:
        return "Medium"

    else:
        return "Low"


# =====================================================
# Home Endpoint
# =====================================================

@app.get("/")
def home():

    return {

        "message": "TeleGuard AI Backend is Running Successfully."

    }

# =====================================================
# Single Prediction
# =====================================================

@app.post("/predict")
def predict(data: CustomerData):

    # -----------------------------
    # Preprocess Input
    # -----------------------------

    df = preprocess_input(data)

    # -----------------------------
    # Prediction
    # -----------------------------

    prediction = int(model.predict(df)[0])

    probability = float(
        model.predict_proba(df)[0][1]
    )

    risk_level = get_risk_level(probability)

    # -----------------------------
    # SHAP Values
    # -----------------------------

    shap_values = explainer.shap_values(df)

    # Handle different SHAP output formats
    if isinstance(shap_values, list):
        shap_row = shap_values[1][0]
    elif len(np.array(shap_values).shape) == 3:
        shap_row = shap_values[0, :, 1]
    else:
        shap_row = shap_values[0]

    feature_impacts = dict(
        zip(
            df.columns,
            shap_row.tolist()
        )
    )

    # -----------------------------
    # Top Churn Reasons
    # -----------------------------

    top_features = sorted(

        feature_impacts.items(),

        key=lambda x: abs(x[1]),

        reverse=True

    )[:5]

    top_reasons = []

    for feature, impact in top_features:

        # Only include features that push toward churn
        if impact <= 0:
            continue

        explanation = translate_feature(feature)

        top_reasons.append({

            "title": explanation["title"],

            "reason": explanation["reason"],

            "recommendation": explanation["recommendation"],

            "impact": round(float(impact), 4)

        })

    # -----------------------------
    # API Response
    # -----------------------------

    return {

        "prediction": prediction,

        "churn_probability": round(
            probability,
            4
        ),

        "risk_level": risk_level,

        "top_reasons": top_reasons

    }

# =====================================================
# Batch Prediction
# =====================================================

@app.post("/predict/batch")
async def predict_batch(file: UploadFile = File(...)):

    # ---------------------------------------
    # Read CSV
    # ---------------------------------------

    contents = await file.read()

    df_raw = pd.read_csv(io.BytesIO(contents))

    # Remove unnecessary columns
    for col in ["customerID", "Churn"]:
        if col in df_raw.columns:
            df_raw.drop(columns=[col], inplace=True)

    # Validate required columns
    missing = [c for c in REQUIRED_COLUMNS if c not in df_raw.columns]

    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Missing columns: {missing}"
        )

    # ---------------------------------------
    # Preprocess
    # ---------------------------------------

    df = preprocess_dataframe(df_raw)

    # ---------------------------------------
    # Prediction
    # ---------------------------------------

    predictions = model.predict(df)

    probabilities = model.predict_proba(df)[:, 1]

    # ---------------------------------------
    # SHAP
    # ---------------------------------------

    shap_values = explainer.shap_values(df)

    if isinstance(shap_values, list):
        shap_matrix = shap_values[1]
    elif len(np.array(shap_values).shape) == 3:
        shap_matrix = shap_values[:, :, 1]
    else:
        shap_matrix = shap_values

    # ---------------------------------------
    # Results
    # ---------------------------------------

    results = []

    driver_counter = Counter()

    for i in range(len(df)):

        probability = float(probabilities[i])

        prediction = int(predictions[i])

        risk = get_risk_level(probability)

        impacts = dict(

            zip(

                df.columns,

                shap_matrix[i].tolist()

            )

        )

        top_features = sorted(

            impacts.items(),

            key=lambda x: abs(x[1]),

            reverse=True

        )[:3]

        translated = []

        for feature, impact in top_features:

            if impact <= 0:
                continue

            explanation = translate_feature(feature)

            translated.append(explanation["title"])

            if risk == "High":
                driver_counter[feature] += 1

        results.append({

            "prediction": prediction,

            "churn_probability": round(probability, 4),

            "risk_level": risk,

            "top_reasons": translated

        })

    # ---------------------------------------
    # Company Health
    # ---------------------------------------

    total = len(results)

    high = sum(r["risk_level"] == "High" for r in results)

    medium = sum(r["risk_level"] == "Medium" for r in results)

    low = sum(r["risk_level"] == "Low" for r in results)

    company_health = {

        "total_customers": total,

        "high_risk_count": high,

        "medium_risk_count": medium,

        "low_risk_count": low,

        "churn_rate": round(high / total, 4) if total else 0

    }

    # ---------------------------------------
    # Top Drivers
    # ---------------------------------------

    top_drivers = []

    for feature, count in driver_counter.most_common(5):

        explanation = translate_feature(feature)

        top_drivers.append({

            "title": explanation["title"],

            "reason": explanation["reason"],

            "recommendation": explanation["recommendation"],

            "affected_customers": count,

            "percentage": round((count / total) * 100, 1) if total else 0

        })

    # ---------------------------------------
    # Business Recommendation
    # ---------------------------------------

    if top_drivers:

        recommended_business_action = get_business_strategy(
            top_drivers[0]
        )

    else:

        recommended_business_action = None

    # ---------------------------------------
    # Executive Summary
    # ---------------------------------------

    if recommended_business_action:

        executive_summary = (
            f"Out of {total} customers analyzed, "
            f"{high} customers ({round(high/total*100,2)}%) "
            f"are at High Risk of churn. "
            f"The primary churn driver is "
            f"{top_drivers[0]['title']}. "
            f"The recommended strategy is "
            f"{recommended_business_action['strategy']}."
        )

    else:

        executive_summary = (
            "No significant churn drivers were detected."
        )

    # ---------------------------------------
    # Final Response
    # ---------------------------------------

    return {

        "company_health": company_health,

        "top_churn_drivers": top_drivers,

        "recommended_business_action":
            recommended_business_action,

        "executive_summary":
            executive_summary,

        "results":
            results

    }