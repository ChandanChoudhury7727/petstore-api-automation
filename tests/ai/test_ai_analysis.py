import allure

from data.factory import generate_pet_payload
from utils.allure_helper import (
    attach_json,
    attach_ai_analysis
)


@allure.epic("Swagger Petstore API")
@allure.feature("AI-Powered API Analysis")
@allure.story("Hugging Face Analysis of Real API Response")
@allure.severity(allure.severity_level.NORMAL)
def test_ai_analyzes_real_api_response(api_client, ai_analyzer):

    payload = generate_pet_payload()

    with allure.step("Create a dynamic Pet"):

        create_response = api_client.create_pet(payload)

    assert create_response.status_code == 200

    created_pet = create_response.json()
    pet_id = created_pet["id"]

    allure.dynamic.parameter(
        "Pet ID",
        str(pet_id)
    )

    attach_json(
        "Created Pet",
        created_pet
    )

    try:

        with allure.step("Delete the dynamic Pet"):

            delete_response = api_client.delete_pet(pet_id)

        assert delete_response.status_code == 200

        with allure.step(
            "Request the deleted Pet to generate a 404 response"
        ):

            response = api_client.get_pet(pet_id)

        response_body = (
            response.json()
            if response.text
            else None
        )

        attach_json(
            "API Response for AI Analysis",
            {
                "status_code": response.status_code,
                "response_body": response_body
            }
        )

        assert response.status_code == 404

        with allure.step(
            "Analyze real API response using Hugging Face"
        ):

            analysis = attach_ai_analysis(
                analyzer=ai_analyzer,
                status_code=response.status_code,
                response_body=response_body
            )

        assert analysis["model"]
        assert analysis["http_status_code"] == response.status_code
        assert analysis["actual_category"]
        assert 0 <= analysis["confidence"] <= 1

    finally:

        cleanup_response = api_client.delete_pet(pet_id)

        if cleanup_response.status_code not in (200, 404):
            attach_json(
                "Unexpected Cleanup Response",
                {
                    "status_code": cleanup_response.status_code,
                    "response": cleanup_response.text
                }
            )