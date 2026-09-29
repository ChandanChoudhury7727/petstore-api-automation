import json
import logging
from typing import Any

import allure
from jsonschema import Draft4Validator

from schemas.openapi_loader import OpenApiLoader

logger = logging.getLogger(__name__)


class OpenApiSchemaValidator:
    """
    Validates API responses against schemas defined
    in the Swagger/OpenAPI specification.
    """

    def __init__(
        self,
        loader: OpenApiLoader | None = None
    ) -> None:

        self.loader = loader or OpenApiLoader()
        self.specification = self.loader.get_specification()

        logger.info(
            "OpenAPI schema validator initialized"
        )

    # ============================================================
    # PUBLIC VALIDATION METHODS
    # ============================================================

    def validate_definition(
        self,
        data: Any,
        definition_name: str
    ) -> None:
        """
        Validate data against a reusable Swagger definition.

        Example:
            Pet
            ApiResponse
            Category
            Tag
        """

        definitions = self.specification.get(
            "definitions",
            {}
        )

        if definition_name not in definitions:
            raise KeyError(
                f"Definition '{definition_name}' was not found "
                f"in the OpenAPI specification."
            )

        schema = self._resolve_schema(
            definitions[definition_name]
        )

        self._validate(
            data=data,
            schema=schema,
            schema_name=definition_name
        )

    def validate_response(
        self,
        endpoint: str,
        method: str,
        status_code: int,
        response_body: Any
    ) -> None:
        """
        Validate an API response against the schema defined
        for the endpoint, HTTP method and status code.
        """

        paths = self.specification.get(
            "paths",
            {}
        )

        if endpoint not in paths:
            raise KeyError(
                f"Endpoint '{endpoint}' was not found "
                f"in the OpenAPI specification."
            )

        method = method.lower()

        operation = paths[endpoint].get(method)

        if operation is None:
            raise KeyError(
                f"HTTP method '{method.upper()}' was not found "
                f"for endpoint '{endpoint}'."
            )

        responses = operation.get(
            "responses",
            {}
        )

        response_definition = (
            responses.get(str(status_code))
            or responses.get("default")
        )

        if response_definition is None:
            raise KeyError(
                f"No response definition found for HTTP "
                f"{status_code} on "
                f"{method.upper()} {endpoint}."
            )

        schema = response_definition.get(
            "schema"
        )

        if schema is None:

            skip_result = {
                "endpoint": endpoint,
                "method": method.upper(),
                "status_code": status_code,
                "validation_status": "SKIPPED",
                "reason": (
                    "Swagger does not define a response schema "
                    "for this endpoint, method, and status code."
                )
            }

            allure.attach(
                json.dumps(
                    skip_result,
                    indent=2,
                    ensure_ascii=False
                ),
                name="Schema Validation Skipped",
                attachment_type=allure.attachment_type.JSON
            )

            logger.warning(
                "Swagger defines HTTP %s for %s %s, "
                "but no response schema is provided. "
                "Response schema validation skipped.",
                status_code,
                method.upper(),
                endpoint
            )
            return

        resolved_schema = self._resolve_schema(
            schema
        )

        self._validate(
            data=response_body,
            schema=resolved_schema,
            schema_name=(
                f"{method.upper()} "
                f"{endpoint} "
                f"HTTP {status_code}"
            )
        )

    # ============================================================
    # INTERNAL SCHEMA RESOLUTION
    # ============================================================

    def _resolve_schema(
        self,
        schema: Any
    ) -> Any:
        """
        Resolve local Swagger references such as:

        #/definitions/Pet
        #/definitions/ApiResponse
        #/definitions/Category
        #/definitions/Tag
        """

        if isinstance(schema, list):
            return [
                self._resolve_schema(item)
                for item in schema
            ]

        if not isinstance(schema, dict):
            return schema

        if "$ref" in schema:
            reference = schema["$ref"]

            if not reference.startswith(
                "#/definitions/"
            ):
                raise ValueError(
                    f"Unsupported Swagger reference: "
                    f"{reference}"
                )

            definition_name = (
                reference.split(
                    "#/definitions/",
                    1
                )[1]
            )

            definitions = self.specification.get(
                "definitions",
                {}
            )

            if definition_name not in definitions:
                raise KeyError(
                    f"Referenced definition "
                    f"'{definition_name}' was not found."
                )

            return self._resolve_schema(
                definitions[definition_name]
            )

        return {
            key: self._resolve_schema(value)
            for key, value in schema.items()
        }

    # ============================================================
    # JSON SCHEMA VALIDATION
    # ============================================================

    def _validate(
        self,
        data: Any,
        schema: dict[str, Any],
        schema_name: str
    ) -> None:
        """
        Validate data against a JSON Schema.

        Attach the validation result to Allure, including
        detailed errors when validation fails.
        """

        validator = Draft4Validator(schema)

        errors = sorted(
            validator.iter_errors(data),
            key=lambda error: list(error.path)
        )

        # --------------------------------------------------------
        # Validation passed
        # --------------------------------------------------------

        if not errors:

            validation_result = {
                "schema": schema_name,
                "validation_status": "PASSED",
                "error_count": 0,
                "errors": []
            }

            allure.attach(
                json.dumps(
                    validation_result,
                    indent=2,
                    ensure_ascii=False
                ),
                name=f"Schema Validation - {schema_name}",
                attachment_type=allure.attachment_type.JSON
            )

            logger.info(
                "JSON Schema validation passed: %s",
                schema_name
            )

            return

        # --------------------------------------------------------
        # Validation failed
        # --------------------------------------------------------

        error_details = []

        for error in errors:

            location = ".".join(
                str(item)
                for item in error.path
            )

            if not location:
                location = "root"

            error_details.append({
                "location": location,
                "message": error.message
            })

        validation_result = {
            "schema": schema_name,
            "validation_status": "FAILED",
            "error_count": len(error_details),
            "errors": error_details
        }

        # Attach detailed validation failure to Allure.
        allure.attach(
            json.dumps(
                validation_result,
                indent=2,
                ensure_ascii=False,
                default=str
            ),
            name=f"Schema Validation Failure - {schema_name}",
            attachment_type=allure.attachment_type.JSON
        )

        error_messages = [
            f"{error['location']}: {error['message']}"
            for error in error_details
        ]

        message = (
            f"JSON Schema validation failed for {schema_name}:\n"
            + "\n".join(error_messages)
        )

        logger.error(message)

        raise AssertionError(message)