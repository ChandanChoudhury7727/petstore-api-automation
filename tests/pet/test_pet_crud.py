import allure

from data.factory import generate_pet_payload
from utils.allure_helper import (
    attach_json,
    attach_ai_analysis
)




@allure.epic("Swagger Petstore API")
@allure.feature("Pet Management")
@allure.story("Pet CRUD Lifecycle")
@allure.severity(allure.severity_level.CRITICAL)
def test_pet_crud_lifecycle(
    api_client,
    ai_analyzer,
    schema_validator
):
    """
    Validate the complete Pet CRUD lifecycle using dynamically
    generated test data.

    Flow:
        POST -> GET -> PUT -> GET -> DELETE -> GET
    """

    payload = generate_pet_payload()
    pet_id = None

    try:
        # ============================================================
        # CREATE
        # ============================================================

        with allure.step("Generate dynamic Pet test data"):
            attach_json(
                "Generated Pet Payload",
                payload
            )

            allure.dynamic.parameter(
                "generated_pet_name",
                payload["name"]
            )

        with allure.step("Create Pet using POST /pet"):
            create_response = api_client.create_pet(payload)

        with allure.step("Validate Pet creation response"):
            assert create_response.status_code == 200, (
                f"Expected HTTP 200 for Pet creation but received "
                f"{create_response.status_code}. "
                f"Response: {create_response.text}"
            )

            schema_validator.validate_definition(
                data=create_response.json(),
                definition_name="Pet"
            )

        created_pet = create_response.json()

        attach_ai_analysis(
            analyzer=ai_analyzer,
            status_code=create_response.status_code,
            response_body=created_pet,
            expected_category="successful API response"
        )

        attach_json(
            "Created Pet Response",
            created_pet
        )

        with allure.step("Capture dynamically generated Pet ID"):
            pet_id = created_pet.get("id")

            assert pet_id is not None, (
                "Petstore did not return a Pet ID after creation."
            )

            assert isinstance(pet_id, int), (
                f"Expected Pet ID to be an integer but received: "
                f"{pet_id}"
            )

            allure.dynamic.parameter(
                "pet_id",
                pet_id
            )

        # ============================================================
        # GET CREATED PET
        # ============================================================

        with allure.step(
            f"Retrieve newly created Pet using ID {pet_id}"
        ):
            get_response = api_client.get_pet(pet_id)

        with allure.step("Validate GET response"):
            assert get_response.status_code == 200, (
                f"Expected HTTP 200 when retrieving Pet {pet_id} "
                f"but received {get_response.status_code}. "
                f"Response: {get_response.text}"
            )

        retrieved_pet = get_response.json()

        attach_ai_analysis(
            analyzer=ai_analyzer,
            status_code=get_response.status_code,
            response_body=retrieved_pet,
            expected_category="successful API response"
        )

        attach_json(
            "Retrieved Created Pet",
            retrieved_pet
        )

        with allure.step("Verify created Pet ID"):
            assert retrieved_pet.get("id") == pet_id, (
                f"Expected Pet ID {pet_id}, "
                f"but received {retrieved_pet.get('id')}"
            )

        with allure.step("Verify created Pet name"):
            assert retrieved_pet.get("name") == payload["name"], (
                f"Expected Pet name '{payload['name']}', "
                f"but received '{retrieved_pet.get('name')}'"
            )

        # ============================================================
        # UPDATE
        # ============================================================

        updated_payload = payload.copy()
        updated_payload["name"] = f"{payload['name']}-Updated"

        with allure.step("Generate updated Pet data"):
            attach_json(
                "Updated Pet Payload",
                updated_payload
            )

        with allure.step("Update Pet using PUT /pet"):
            update_response = api_client.update_pet(
                updated_payload
            )

        with allure.step("Validate Pet update response"):
            assert update_response.status_code == 200, (
                f"Expected HTTP 200 for Pet update but received "
                f"{update_response.status_code}. "
                f"Response: {update_response.text}"
            )

            schema_validator.validate_definition(
                data=update_response.json(),
                definition_name="Pet"
            )

        updated_pet = update_response.json()

        attach_ai_analysis(
            analyzer=ai_analyzer,
            status_code=update_response.status_code,
            response_body=updated_pet,
            expected_category="successful API response"
        )

        attach_json(
            "Updated Pet Response",
            updated_pet
        )

        with allure.step("Verify updated Pet ID"):
            assert updated_pet.get("id") == pet_id, (
                f"Expected updated Pet ID {pet_id}, "
                f"but received {updated_pet.get('id')}"
            )

        with allure.step("Verify updated Pet name"):
            assert updated_pet.get("name") == updated_payload["name"], (
                f"Expected updated Pet name "
                f"'{updated_payload['name']}', "
                f"but received '{updated_pet.get('name')}'"
            )

        # ============================================================
        # GET UPDATED PET
        # ============================================================

        with allure.step(
            f"Retrieve updated Pet using ID {pet_id}"
        ):
            updated_get_response = api_client.get_pet(pet_id)

        with allure.step("Validate updated GET response"):
            assert updated_get_response.status_code == 200, (
                f"Expected HTTP 200 when retrieving updated Pet "
                f"{pet_id} but received "
                f"{updated_get_response.status_code}. "
                f"Response: {updated_get_response.text}"
            )

            schema_validator.validate_response(
                endpoint="/pet/{petId}",
                method="GET",
                status_code=updated_get_response.status_code,
                response_body=updated_get_response.json()
            )

        updated_pet_details = updated_get_response.json()

        attach_ai_analysis(
            analyzer=ai_analyzer,
            status_code=updated_get_response.status_code,
            response_body=updated_pet_details,
            expected_category="successful API response"
        )

        attach_json(
            "Updated Pet Retrieved From API",
            updated_pet_details
        )

        with allure.step("Verify updated data persisted"):
            assert updated_pet_details.get("name") == (
                updated_payload["name"]
            ), (
                f"Updated Pet name was not persisted. "
                f"Expected '{updated_payload['name']}', "
                f"received '{updated_pet_details.get('name')}'"
            )

        # ============================================================
        # DELETE
        # ============================================================

        with allure.step(
            f"Delete Pet using DELETE /pet/{pet_id}"
        ):
            delete_response = api_client.delete_pet(pet_id)

        with allure.step("Validate Pet deletion response"):
            assert delete_response.status_code == 200, (
                f"Expected HTTP 200 for Pet deletion but received "
                f"{delete_response.status_code}. "
                f"Response: {delete_response.text}"
            )

        delete_body = (
            delete_response.json()
            if delete_response.text
            else None
        )

        attach_ai_analysis(
            analyzer=ai_analyzer,
            status_code=delete_response.status_code,
            response_body=delete_body,
            expected_category="successful API response"
        )

        attach_json(
            "Delete Pet Response",
            {
                "status_code": delete_response.status_code,
                "body": delete_response.text
            }
        )

        # ============================================================
        # VERIFY DELETE
        # ============================================================

        with allure.step(
            f"Verify Pet {pet_id} no longer exists"
        ):
            verify_delete_response = api_client.get_pet(pet_id)

        with allure.step("Validate deleted Pet response"):
            assert verify_delete_response.status_code == 404, (
                f"Expected HTTP 404 after deleting Pet {pet_id}, "
                f"but received "
                f"{verify_delete_response.status_code}. "
                f"Response: {verify_delete_response.text}"
            )

            not_found_body = (
                verify_delete_response.json()
                if verify_delete_response.text
                else None
            )

            attach_ai_analysis(
                analyzer=ai_analyzer,
                status_code=verify_delete_response.status_code,
                response_body=not_found_body,
                expected_category="not found error"
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
                            f"Cleanup attempted for Pet ID {pet_id}. "
                            f"HTTP status: "
                            f"{cleanup_response.status_code}"
                        ),
                        name="Final Cleanup",
                        attachment_type=allure.attachment_type.TEXT
                    )
                else:
                    allure.attach(
                        (
                            f"Cleanup DELETE for Pet ID {pet_id} "
                            f"returned unexpected HTTP status "
                            f"{cleanup_response.status_code}. "
                            f"Response: {cleanup_response.text}"
                        ),
                        name="Cleanup Warning",
                        attachment_type=allure.attachment_type.TEXT
                    )

            except Exception as cleanup_error:
                allure.attach(
                    str(cleanup_error),
                    name="Cleanup Exception",
                    attachment_type=allure.attachment_type.TEXT
                )