import requests
from config import API_URL

def check_backend_health():
    try:
        response = requests.get(API_URL, timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
# ---------------------------------
# Single Prediction
# ---------------------------------

def predict_customer(data):

    response = requests.post(
        f"{API_URL}/predict",
        json=data
    )

    response.raise_for_status()

    return response.json()


# ---------------------------------
# Batch Prediction
# ---------------------------------

def predict_batch(file):

    files = {
        "file": (
            file.name,
            file,
            "text/csv"
        )
    }

    response = requests.post(
        f"{API_URL}/predict/batch",
        files=files
    )

    response.raise_for_status()

    return response.json()