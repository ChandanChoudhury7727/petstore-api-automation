import allure

from data.factory import generate_pet_payload
from utils.allure_helper import (
    attach_json,
    attach_ai_analysis
)


@allure.epic("Swagger Petstore API")
@allure.feature("Pet Management")
@allure.story("Negative API Testing")
@allure.severity(allure.severity_level.NORMAL)
def test_get_deleted_pet_returns_404(
    api_client,
    ai_analyzer
):
    """
    Verify that attempting to retrieve a Pet after it has been
    deleted returns HTTP 404.

    The Pet ID is generated dynamically during test execution.
    """

    payload = generate_pet_payload()
    pet_id = None

    try:
        # ============================================================
        # CREATE PET
        # ============================================================

        with allure.step("Generate dynamic Pet for negative testing"):
            attach_json(
                "Negative Test Pet Payload",
                payload
            )

        with allure.step("Create Pet"):
            create_response = api_client.create_pet(payload)

        with allure.step("Validate Pet creation"):
            assert create_response.status_code == 200, (
                f"Expected HTTP 200 when creating Pet, "
                f"but received {create_response.status_code}. "
                f"Response: {create_response.text}"
            )

        created_pet = create_response.json()

        attach_json(
            "Created Pet For Negative Test",
            created_pet
        )

        pet_id = created_pet.get("id")

        assert isinstance(pet_id, int), (
            f"Petstore did not return a valid integer Pet ID: "
            f"{created_pet}"
        )

        allure.dynamic.parameter("pet_id", pet_id)

        # ============================================================
        # DELETE PET
        # ============================================================

        with allure.step(
            f"Delete Pet {pet_id} before negative GET test"
        ):
            delete_response = api_client.delete_pet(pet_id)

        with allure.step("Validate deletion"):
            assert delete_response.status_code == 200, (
                f"Expected HTTP 200 when deleting Pet {pet_id}, "
                f"but received {delete_response.status_code}. "
                f"Response: {delete_response.text}"
            )

        attach_json(
            "Initial Delete Response",
            {
                "status_code": delete_response.status_code,
                "body": delete_response.text
            }
        )

        # ============================================================
        # NEGATIVE GET
        # ============================================================

        with allure.step(
            f"Attempt GET for deleted Pet {pet_id}"
        ):
            get_response = api_client.get_pet(pet_id)

        response_body = (
            get_response.json()
            if get_response.text
            else None
        )

        attach_ai_analysis(
            analyzer=ai_analyzer,
            status_code=get_response.status_code,
            response_body=response_body
        )

        with allure.step("Validate expected 404 response"):
            assert get_response.status_code == 404, (
                f"Expected HTTP 404 for deleted Pet {pet_id}, "
                f"but received {get_response.status_code}. "
                f"Response: {get_response.text}"
            )

        negative_response = {
            "status_code": get_response.status_code,
            "body": get_response.text
        }

        attach_json(
            "Expected Negative GET Response",
            negative_response
        )

        with allure.step("Validate error response body"):
            error_body = get_response.json()

            assert isinstance(error_body, dict), (
                f"Expected error response to be a JSON object, "
                f"but received: {error_body}"
            )

            assert error_body.get("message") == "Pet not found", (
                f"Expected error message 'Pet not found', "
                f"but received: {error_body}"
            )

    finally:
        # ============================================================
        # SAFETY CLEANUP
        # ============================================================

        if pet_id is not None:
            try:
                cleanup_response = api_client.delete_pet(pet_id)

                if cleanup_response.status_code in (200, 404):
                    allure.attach(
                        (
                            f"Negative GET test cleanup for Pet ID "
                            f"{pet_id}. HTTP status: "
                            f"{cleanup_response.status_code}"
                        ),
                        name="Negative Test Cleanup",
                        attachment_type=allure.attachment_type.TEXT
                    )
                else:
                    allure.attach(
                        (
                            f"Cleanup returned unexpected HTTP status "
                            f"{cleanup_response.status_code} for Pet "
                            f"ID {pet_id}. Response: "
                            f"{cleanup_response.text}"
                        ),
                        name="Negative Test Cleanup Warning",
                        attachment_type=allure.attachment_type.TEXT
                    )

            except Exception as cleanup_error:
                allure.attach(
                    str(cleanup_error),
                    name="Negative Test Cleanup Exception",
                    attachment_type=allure.attachment_type.TEXT
                )


@allure.epic("Swagger Petstore API")
@allure.feature("Pet API")
@allure.story("Negative API Testing")
@allure.severity(allure.severity_level.NORMAL)
def test_delete_already_deleted_pet_returns_404(
    api_client,
    ai_analyzer
):
    """
    Verify that attempting to delete a Pet that has already been
    deleted returns HTTP 404.

    The Pet ID is generated dynamically during test execution.
    """

    payload = generate_pet_payload()
    pet_id = None

    # ================================================================
    # CREATE PET
    # ================================================================

    with allure.step("Generate dynamic Pet"):
        attach_json(
            "Delete Negative Test Payload",
            payload
        )

    with allure.step("Create Pet"):
        create_response = api_client.create_pet(payload)

    assert create_response.status_code == 200, (
        f"Expected HTTP 200 when creating Pet, "
        f"but received {create_response.status_code}. "
        f"Response: {create_response.text}"
    )

    created_pet = create_response.json()

    attach_json(
        "Created Pet For Delete Negative Test",
        created_pet
    )

    pet_id = created_pet.get("id")

    assert isinstance(pet_id, int), (
        f"Petstore did not return a valid integer Pet ID: "
        f"{created_pet}"
    )

    allure.dynamic.parameter("pet_id", pet_id)

    try:
        # ============================================================
        # FIRST DELETE
        # ============================================================

        with allure.step(
            f"Delete Pet {pet_id}"
        ):
            first_delete_response = api_client.delete_pet(pet_id)

        with allure.step("Validate first deletion"):
            assert first_delete_response.status_code == 200, (
                f"Expected HTTP 200 for first DELETE of Pet {pet_id}, "
                f"but received {first_delete_response.status_code}. "
                f"Response: {first_delete_response.text}"
            )

        attach_json(
            "First Delete Response",
            {
                "status_code": first_delete_response.status_code,
                "body": first_delete_response.text
            }
        )

        # ============================================================
        # SECOND DELETE — NEGATIVE TEST
        # ============================================================

        with allure.step(
            f"Attempt second DELETE for already deleted Pet {pet_id}"
        ):
            second_delete_response = api_client.delete_pet(pet_id)

        response_body = (
            second_delete_response.json()
            if second_delete_response.text
            else None
        )

        attach_ai_analysis(
            analyzer=ai_analyzer,
            status_code=second_delete_response.status_code,
            response_body=response_body
        )

        with allure.step("Validate expected 404 response"):
            assert second_delete_response.status_code == 404, (
                f"Expected HTTP 404 when deleting already deleted "
                f"Pet {pet_id}, but received "
                f"{second_delete_response.status_code}. "
                f"Response: {second_delete_response.text}"
            )

        attach_json(
            "Expected Negative DELETE Response",
            {
                "status_code": second_delete_response.status_code,
                "body": second_delete_response.text
            }
        )

    finally:
        # ============================================================
        # SAFETY CLEANUP
        # ============================================================

        if pet_id is not None:
            try:
                cleanup_response = api_client.delete_pet(pet_id)

                if cleanup_response.status_code in (200, 404):
                    allure.attach(
                        (
                            f"Negative DELETE test cleanup for Pet ID "
                            f"{pet_id}. HTTP status: "
                            f"{cleanup_response.status_code}"
                        ),
                        name="Negative Delete Test Cleanup",
                        attachment_type=allure.attachment_type.TEXT
                    )

            except Exception as cleanup_error:
                allure.attach(
                    str(cleanup_error),
                    name="Negative Delete Cleanup Exception",
                    attachment_type=allure.attachment_type.TEXT
                )