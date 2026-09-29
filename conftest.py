import json
import logging
import platform
import sys
from pathlib import Path

import allure
import pytest

from ai.analyzer import ApiResponseAnalyzer
from api.pet_api import PetApi
from config.settings import (
    AI_MODEL_NAME,
    BASE_URL,
    OPENAPI_URL,
)
from data.factory import generate_pet_payload
from utils.allure_helper import attach_api_history
from utils.logger import configure_logging
from schemas.response_validator import OpenApiSchemaValidator


# ============================================================
# LOGGING
# ============================================================

configure_logging()

logger = logging.getLogger(__name__)


# ============================================================
# ALLURE ENVIRONMENT
# ============================================================

def pytest_sessionstart(session):
    """
    Runs once when the pytest session starts.

    Creates Allure environment information.
    """

    results_dir = Path("allure-results")
    results_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    environment_file = (
        results_dir / "environment.properties"
    )

    environment_data = [
        f"Python={platform.python_version()}",
        f"OperatingSystem={platform.system()} {platform.release()}",
        f"Platform={platform.platform()}",
        f"PythonExecutable={sys.executable}",
        f"API=Swagger Petstore",
        f"BaseURL={BASE_URL}",
        f"OpenAPIURL={OPENAPI_URL}",
        f"AIModel={AI_MODEL_NAME}",
    ]

    environment_file.write_text(
        "\n".join(environment_data),
        encoding="utf-8"
    )

    logger.info(
        "Allure environment information created"
    )


# ============================================================
# API CLIENT FIXTURE
# ============================================================

@pytest.fixture
def api_client():
    """
    Provides a fresh PetApi client for each test.
    """

    logger.info(
        "Creating Pet API client"
    )

    return PetApi(BASE_URL)


# ============================================================
# HUGGING FACE AI FIXTURE
# ============================================================

@pytest.fixture(scope="session")
def ai_analyzer():
    """
    Creates the Hugging Face analyzer once per pytest session.

    This prevents the AI model from being loaded separately
    for every test.
    """

    logger.info(
        "Creating session-level Hugging Face analyzer"
    )

    analyzer = ApiResponseAnalyzer()

    logger.info(
        "Hugging Face analyzer is ready"
    )

    return analyzer

# ============================================================
# OPENAPI / JSON SCHEMA VALIDATOR FIXTURE
# ============================================================

@pytest.fixture(scope="session")
def schema_validator():
    """
    Creates the OpenAPI schema validator once per pytest session.

    The validator loads the Swagger/OpenAPI specification
    and validates API responses against the defined schemas.
    """

    logger.info(
        "Creating session-level OpenAPI schema validator"
    )

    validator = OpenApiSchemaValidator()

    logger.info(
        "OpenAPI schema validator is ready"
    )

    return validator


# ============================================================
# DYNAMIC PET FIXTURE
# ============================================================

@pytest.fixture
def created_pet(api_client):
    """
    Creates a dynamic Pet before a test and deletes it
    automatically after the test.

    This fixture is useful for tests that need an existing
    Pet resource.
    """

    payload = generate_pet_payload()

    logger.info(
        "Creating dynamic Pet: %s",
        payload["name"]
    )

    response = api_client.create_pet(payload)

    assert response.status_code == 200, (
        "Dynamic Pet creation failed. "
        f"Status: {response.status_code}, "
        f"Response: {response.text}"
    )

    created_pet = response.json()

    pet_id = created_pet.get("id")

    assert pet_id is not None, (
        "Petstore did not return a Pet ID "
        "after successful creation."
    )

    logger.info(
        "Dynamic Pet created successfully. ID: %s",
        pet_id
    )

    try:
        yield created_pet

    finally:
        logger.info(
            "Cleaning up dynamic Pet. ID: %s",
            pet_id
        )

        cleanup_response = api_client.delete_pet(
            pet_id
        )

        logger.info(
            "Cleanup DELETE response: %s",
            cleanup_response.status_code
        )


# ============================================================
# API HISTORY → ALLURE
# ============================================================

@pytest.fixture(autouse=True)
def attach_test_api_history(request):
    yield

    api_client_fixture = request.node.funcargs.get("api_client")

    if api_client_fixture is None:
        return

    if not api_client_fixture.history:
        return

    logger.info(
        "Attaching %s API call(s) to Allure for test: %s",
        len(api_client_fixture.history),
        request.node.name
    )

    attach_api_history(api_client_fixture.history)