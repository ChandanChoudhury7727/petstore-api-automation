import logging
from typing import Any

import requests

from config.settings import OPENAPI_URL, REQUEST_TIMEOUT


logger = logging.getLogger(__name__)


class OpenApiLoader:
    """
    Loads the Swagger Petstore OpenAPI specification.

    The specification is retrieved dynamically from the configured
    OpenAPI URL instead of being manually copied into the project.
    """

    def __init__(self, openapi_url: str = OPENAPI_URL):
        self.openapi_url = openapi_url
        self.specification: dict[str, Any] | None = None

    def load(self) -> dict[str, Any]:
        """
        Download and return the OpenAPI specification.
        """

        logger.info(
            "Loading OpenAPI specification from: %s",
            self.openapi_url
        )

        response = requests.get(
            self.openapi_url,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        specification = response.json()

        if not isinstance(specification, dict):
            raise ValueError(
                "OpenAPI specification must be a JSON object."
            )

        self.specification = specification

        logger.info(
            "OpenAPI specification loaded successfully."
        )

        return specification

    def get_specification(self) -> dict[str, Any]:
        """
        Return the already-loaded specification.

        If it has not been loaded yet, load it automatically.
        """

        if self.specification is None:
            return self.load()

        return self.specification

    def get_paths(self) -> dict[str, Any]:
        """
        Return all API paths from the OpenAPI specification.
        """

        specification = self.get_specification()

        return specification.get("paths", {})

    def get_definitions(self) -> dict[str, Any]:
        """
        Return model definitions from Swagger/OpenAPI 2.0.
        """

        specification = self.get_specification()

        return specification.get("definitions", {})