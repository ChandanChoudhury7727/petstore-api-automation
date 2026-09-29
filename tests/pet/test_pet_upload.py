from pathlib import Path

import allure

from data.factory import generate_pet_payload
from utils.allure_helper import (
    attach_json,
    attach_ai_analysis
)


IMAGE_PATH = (
    Path(__file__).resolve().parents[2]
    / "test_data"
    / "images"
    / "pet_test_image.png"
)


@allure.epic("Swagger Petstore API")
@allure.feature("Pet Management")
@allure.story("Pet Image Upload")
@allure.severity(allure.severity_level.NORMAL)
def test_upload_pet_image(
    api_client,
    ai_analyzer,
    schema_validator
):
    """
    Verify that an image can be uploaded for a dynamically
    created Pet.

    The Pet ID is generated dynamically.
    The image is loaded from the project's test data directory.
    """

    payload = generate_pet_payload()
    pet_id = None

    try:
        # ============================================================
        # VALIDATE TEST IMAGE
        # ============================================================

        with allure.step("Validate test image exists"):

            assert IMAGE_PATH.exists(), (
                f"Test image was not found: {IMAGE_PATH}"
            )

            assert IMAGE_PATH.is_file(), (
                f"Test image path is not a file: {IMAGE_PATH}"
            )

            allure.dynamic.parameter(
                "image_file",
                IMAGE_PATH.name
            )

            allure.attach(
                str(IMAGE_PATH),
                name="Upload Image Path",
                attachment_type=allure.attachment_type.TEXT
            )

        # ============================================================
        # CREATE PET
        # ============================================================

        with allure.step("Generate dynamic Pet payload"):

            attach_json(
                "Upload Test Pet Payload",
                payload
            )

        with allure.step("Create Pet for image upload"):

            create_response = api_client.create_pet(payload)

        with allure.step("Validate Pet creation response"):

            assert create_response.status_code == 200, (
                f"Expected HTTP 200 when creating Pet, "
                f"but received {create_response.status_code}. "
                f"Response: {create_response.text}"
            )

        created_pet = create_response.json()

        attach_json(
            "Created Pet For Image Upload",
            created_pet
        )

        pet_id = created_pet.get("id")

        assert isinstance(pet_id, int), (
            f"Petstore did not return a valid integer Pet ID: "
            f"{created_pet}"
        )

        allure.dynamic.parameter(
            "pet_id",
            pet_id
        )

        # ============================================================
        # IMAGE UPLOAD
        # ============================================================

        with allure.step(
            f"Upload image for dynamically created Pet {pet_id}"
        ):

            upload_response = api_client.upload_image(
                pet_id=pet_id,
                file_path=str(IMAGE_PATH),
                metadata="Automated Pet image upload"
            )

        upload_body = (
            upload_response.json()
            if upload_response.text
            else None
        )

        attach_json(
            "Pet Upload Response",
            {
                "status_code": upload_response.status_code,
                "response_body": upload_body
            }
        )

        with allure.step(
            "Analyze Pet upload response using Hugging Face"
        ):

            analysis = attach_ai_analysis(
                analyzer=ai_analyzer,
                status_code=upload_response.status_code,
                response_body=upload_body
            )

        with allure.step("Validate image upload HTTP response"):

            assert upload_response.status_code == 200, (
                f"Expected HTTP 200 for image upload, "
                f"but received {upload_response.status_code}. "
                f"Response: {upload_response.text}"
            )

        schema_validator.validate_response(
            endpoint="/pet/{petId}/uploadImage",
            method="POST",
            status_code=upload_response.status_code,
            response_body=upload_body
        )

        # ============================================================
        # VALIDATE UPLOAD RESPONSE
        # ============================================================

        with allure.step("Validate upload response structure"):

            assert isinstance(upload_body, dict), (
                f"Expected upload response to be a JSON object, "
                f"but received: {upload_body}"
            )

            assert "code" in upload_body, (
                f"Upload response is missing 'code': {upload_body}"
            )

            assert "type" in upload_body, (
                f"Upload response is missing 'type': {upload_body}"
            )

            assert "message" in upload_body, (
                f"Upload response is missing 'message': {upload_body}"
            )

        with allure.step("Record successful upload details"):

            upload_details = {
                "pet_id": pet_id,
                "image": IMAGE_PATH.name,
                "image_size_bytes": IMAGE_PATH.stat().st_size,
                "status_code": upload_response.status_code,
                "response": upload_body,
            }

            attach_json(
                "Image Upload Execution Details",
                upload_details
            )

    finally:
        # ============================================================
        # CLEANUP
        # ============================================================

        if pet_id is not None:

            try:

                with allure.step(
                    f"Cleanup uploaded-image test Pet {pet_id}"
                ):

                    cleanup_response = api_client.delete_pet(
                        pet_id
                    )

                    allure.attach(
                        (
                            f"Cleanup Pet ID: {pet_id}\n"
                            f"HTTP status: "
                            f"{cleanup_response.status_code}\n"
                            f"Response: {cleanup_response.text}"
                        ),
                        name="Upload Test Cleanup",
                        attachment_type=allure.attachment_type.TEXT
                    )

            except Exception as cleanup_error:

                allure.attach(
                    str(cleanup_error),
                    name="Upload Test Cleanup Exception",
                    attachment_type=allure.attachment_type.TEXT
                )