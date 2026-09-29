import os


# ============================================================
# API CONFIGURATION
# ============================================================

BASE_URL = os.getenv(
    "PETSTORE_BASE_URL",
    "https://petstore.swagger.io/v2"
)

OPENAPI_URL = os.getenv(
    "PETSTORE_OPENAPI_URL",
    f"{BASE_URL}/swagger.json"
)


# ============================================================
# REQUEST CONFIGURATION
# ============================================================

REQUEST_TIMEOUT = int(
    os.getenv("API_TIMEOUT", "15")
)


# ============================================================
# AI CONFIGURATION
# ============================================================

AI_MODEL_NAME = os.getenv(
    "AI_MODEL_NAME",
    "typeform/distilbert-base-uncased-mnli"
)