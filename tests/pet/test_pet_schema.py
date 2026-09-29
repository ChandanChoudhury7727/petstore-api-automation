import pytest
import allure

from utils.allure_helper import attach_json


@allure.epic("Swagger Petstore API")
@allure.feature("API Contract Validation")
@allure.story("Valid Pet Schema")
@allure.severity(allure.severity_level.NORMAL)
def test_valid_pet_matches_schema(schema_validator):

    valid_pet = {
        "id": 123456,
        "category": {
            "id": 100,
            "name": "TestCategory"
        },
        "name": "SchemaValidationPet",
        "photoUrls": [
            "https://example.com/test.jpg"
        ],
        "tags": [
            {
                "id": 1,
                "name": "test"
            }
        ],
        "status": "available"
    }

    attach_json(
        "Valid Pet Test Data",
        valid_pet
    )

    with allure.step(
        "Validate valid Pet against Swagger Pet schema"
    ):
        schema_validator.validate_definition(
            data=valid_pet,
            definition_name="Pet"
        )


@allure.epic("Swagger Petstore API")
@allure.feature("API Contract Validation")
@allure.story("Invalid Pet Schema")
@allure.severity(allure.severity_level.NORMAL)
def test_invalid_pet_fails_schema_validation(
    schema_validator
):

    invalid_pet = {
        "id": "NOT_AN_INTEGER",
        "category": {
            "id": 100,
            "name": "TestCategory"
        },
        "name": 12345,
        "photoUrls": [
            "https://example.com/test.jpg"
        ],
        "tags": [],
        "status": "available"
    }

    attach_json(
        "Invalid Pet Test Data",
        invalid_pet
    )

    with allure.step(
        "Verify invalid Pet fails Swagger schema validation"
    ):

        with pytest.raises(
            AssertionError,
            match="JSON Schema validation failed"
        ):

            schema_validator.validate_definition(
                data=invalid_pet,
                definition_name="Pet"
            )