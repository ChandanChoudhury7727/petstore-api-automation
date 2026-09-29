from pathlib import Path
from typing import Any

from api.base_client import BaseApiClient


class PetApi(BaseApiClient):
    """
    API client for Swagger Petstore Pet endpoints.
    """

    def create_pet(
        self,
        payload: dict[str, Any]
    ):
        return self.request(
            "POST",
            "/pet",
            json=payload
        )

    def get_pet(
        self,
        pet_id: int
    ):
        return self.request(
            "GET",
            f"/pet/{pet_id}"
        )

    def update_pet(
        self,
        payload: dict[str, Any]
    ):
        return self.request(
            "PUT",
            "/pet",
            json=payload
        )

    def delete_pet(
        self,
        pet_id: int
    ):
        return self.request(
            "DELETE",
            f"/pet/{pet_id}"
        )

    def find_pets_by_status(
        self,
        status: str
    ):
        return self.request(
            "GET",
            "/pet/findByStatus",
            params={
                "status": status
            }
        )

    def find_pets_by_tags(
        self,
        tags: list[str]
    ):
        return self.request(
            "GET",
            "/pet/findByTags",
            params=[
                ("tags", tag)
                for tag in tags
            ]
        )

    def upload_image(
        self,
        pet_id: int,
        file_path: str,
        metadata: str | None = None
    ):
        file_path = Path(file_path)

        data = {}

        if metadata:
            data["additionalMetadata"] = metadata

        with file_path.open("rb") as image_file:

            files = {
                "file": (
                    file_path.name,
                    image_file
                )
            }

            return self.request(
                "POST",
                f"/pet/{pet_id}/uploadImage",
                files=files,
                data=data
            )