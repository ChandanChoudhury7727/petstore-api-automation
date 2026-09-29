import allure

from utils.allure_helper import (
    attach_json,
    attach_ai_analysis
)




@allure.epic("Swagger Petstore API")
@allure.feature("Pet Management")
@allure.story("Pet Fetch Operations")
@allure.severity(allure.severity_level.NORMAL)
def test_fetch_available_pets(
    api_client,
    ai_analyzer
):
    """
    Verify that the Petstore find-by-status endpoint is available
    and returns a valid list response.

    The public Petstore dataset may contain records with incomplete
    fields. Those records are detected and reported in Allure instead
    of causing this endpoint-level test to fail.
    """

    with allure.step("Request available pets from Petstore"):
        response = api_client.find_pets_by_status("available")

    with allure.step("Validate HTTP response"):
        assert response.status_code == 200, (
            f"Expected HTTP 200 but received {response.status_code}. "
            f"Response: {response.text}"
        )

    with allure.step("Parse API response"):
        pets = response.json()

    attach_ai_analysis(
        analyzer=ai_analyzer,
        status_code=response.status_code,
        response_body=pets
    )

    attach_json("Available Pets Response", pets)

    with allure.step("Validate response is a list"):
        assert isinstance(pets, list), (
            "Expected Petstore response to be a list"
        )

    malformed_records = []

    with allure.step("Validate basic Pet record structure"):
        for pet in pets:
            assert isinstance(pet, dict), (
                f"Each Pet must be a JSON object: {pet}"
            )

            assert "id" in pet, (
                f"Pet is missing required 'id': {pet}"
            )

            assert isinstance(pet["id"], int), (
                f"Pet ID must be an integer: {pet}"
            )

            assert "status" in pet, (
                f"Pet is missing 'status': {pet}"
            )

            assert pet["status"] == "available", (
                f"Expected status 'available' but received "
                f"'{pet['status']}' for Pet ID {pet['id']}"
            )

            # Detect incomplete live data without failing the endpoint test.
            if not pet.get("name"):
                malformed_records.append({
                    "id": pet.get("id"),
                    "missing_field": "name",
                    "record": pet
                })

    if malformed_records:
        attach_json(
            "Detected Incomplete Pet Records",
            malformed_records
        )

        allure.attach(
            (
                f"Detected {len(malformed_records)} available Pet record(s) "
                "without a name. "
                "The endpoint returned HTTP 200 successfully, so this is "
                "reported as a live data-quality issue rather than an "
                "endpoint availability failure."
            ),
            name="Data Quality Observation",
            attachment_type=allure.attachment_type.TEXT
        )


@allure.epic("Swagger Petstore API")
@allure.feature("Pet API")
@allure.story("Fetch Pet Using Dynamic API Data")
@allure.severity(allure.severity_level.CRITICAL)
def test_fetch_pet_using_dynamic_id(
    api_client,
    schema_validator,
    ai_analyzer
):
    """
    Discover a valid Pet dynamically from the API and fetch it by ID.

    No Pet ID is hard-coded.
    """

    with allure.step("Fetch available Pets to obtain a dynamic Pet ID"):
        response = api_client.find_pets_by_status("available")

    assert response.status_code == 200, (
        f"Expected HTTP 200 but received {response.status_code}. "
        f"Response: {response.text}"
    )
    

    pets = response.json()

    attach_json(
        "Pets Used For Dynamic ID Selection",
        pets
    )

    with allure.step("Find a valid Pet dynamically"):
        pet = next(
            (
                item
                for item in pets
                if (
                    isinstance(item, dict)
                    and isinstance(item.get("id"), int)
                    and isinstance(item.get("name"), str)
                    and bool(item["name"].strip())
                    and item.get("status") == "available"
                )
            ),
            None
        )

    assert pet is not None, (
        "No valid available Pet with ID and name was returned "
        "by Petstore. Unable to perform dynamic GET test."
    )

    pet_id = pet["id"]

    allure.dynamic.parameter("pet_id", pet_id)

    with allure.step(
        f"GET Pet using dynamically discovered ID: {pet_id}"
    ):
        pet_response = api_client.get_pet(pet_id)

    with allure.step("Validate dynamic Pet GET response"):
        assert pet_response.status_code == 200, (
            f"Expected HTTP 200 when fetching Pet ID {pet_id}, "
            f"but received {pet_response.status_code}. "
            f"Response: {pet_response.text}"
        )

        schema_validator.validate_response(
            endpoint="/pet/{petId}",
            method="GET",
            status_code=pet_response.status_code,
            response_body=pet_response.json()
        )

    pet_details = pet_response.json()

    attach_ai_analysis(
        analyzer=ai_analyzer,
        status_code=pet_response.status_code,
        response_body=pet_details
    )

    attach_json(
        "Dynamically Retrieved Pet",
        pet_details
    )

    with allure.step("Validate returned Pet ID"):
        assert pet_details.get("id") == pet_id, (
            f"Expected Pet ID {pet_id}, "
            f"but received {pet_details.get('id')}"
        )

    with allure.step("Validate returned Pet name"):
        assert "name" in pet_details, (
            f"Pet ID {pet_id} response is missing 'name': "
            f"{pet_details}"
        )

        assert isinstance(pet_details["name"], str), (
            f"Pet name must be a string: {pet_details}"
        )

        assert pet_details["name"].strip(), (
            f"Pet name must not be empty: {pet_details}"
        )

    with allure.step("Validate returned Pet status"):
        assert "status" in pet_details, (
            f"Pet ID {pet_id} response is missing 'status': "
            f"{pet_details}"
        )

    with allure.step("Validate returned Pet status is available"):
        assert pet_details["status"] == "available", (
            f"Expected Pet ID {pet_id} to have status 'available', "
            f"but received '{pet_details['status']}'"
        )