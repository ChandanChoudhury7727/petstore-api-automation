import json
import logging
import time
from pathlib import Path
from typing import Any

import requests

from config.settings import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


class BaseApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.history: list[dict[str, Any]] = []

    def request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any
    ) -> requests.Response:

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        kwargs.setdefault("timeout", REQUEST_TIMEOUT)

        request_body = kwargs.get("json")
        request_params = kwargs.get("params")
        request_headers = kwargs.get("headers")
        request_data = kwargs.get("data")
        request_files = kwargs.get("files")

        logger.info(
            "REQUEST: %s %s",
            method.upper(),
            url
        )

        # ------------------------------------------------------------
        # Request parameters
        # ------------------------------------------------------------

        if request_params:
            logger.info(
                "REQUEST PARAMS: %s",
                json.dumps(
                    request_params,
                    default=str
                )
            )

        # ------------------------------------------------------------
        # Request headers
        # ------------------------------------------------------------

        if request_headers:
            logger.info(
                "REQUEST HEADERS: %s",
                json.dumps(
                    request_headers,
                    default=str
                )
            )

        # ------------------------------------------------------------
        # JSON request body
        # ------------------------------------------------------------

        if request_body is not None:
            logger.info(
                "REQUEST BODY: %s",
                json.dumps(
                    request_body,
                    indent=2,
                    default=str
                )
            )

        # ------------------------------------------------------------
        # Form/multipart data
        # ------------------------------------------------------------

        if request_data:
            logger.info(
                "REQUEST FORM DATA: %s",
                json.dumps(
                    request_data,
                    indent=2,
                    default=str
                )
            )

        # ------------------------------------------------------------
        # Multipart file information
        #
        # Do NOT log binary file contents.
        # Only log safe metadata.
        # ------------------------------------------------------------

        file_metadata = {}

        if request_files:
            for field_name, file_value in request_files.items():

                if isinstance(file_value, tuple):
                    filename = (
                        file_value[0]
                        if len(file_value) > 0
                        else None
                    )

                    file_object = (
                        file_value[1]
                        if len(file_value) > 1
                        else None
                    )

                    content_type = (
                        file_value[2]
                        if len(file_value) > 2
                        else None
                    )

                    file_size = None

                    if hasattr(file_object, "fileno"):
                        try:
                            current_position = file_object.tell()
                            file_size = Path(
                                file_object.name
                            ).stat().st_size

                            file_object.seek(current_position)

                        except (OSError, ValueError):
                            file_size = None

                    file_metadata[field_name] = {
                        "filename": filename,
                        "content_type": content_type,
                        "size_bytes": file_size
                    }

                else:
                    file_metadata[field_name] = {
                        "value_type": type(file_value).__name__
                    }

            logger.info(
                "REQUEST FILES: %s",
                json.dumps(
                    file_metadata,
                    indent=2,
                    default=str
                )
            )

        start_time = time.perf_counter()

        try:
            response = self.session.request(
                method=method,
                url=url,
                **kwargs
            )

            duration_ms = round(
                (time.perf_counter() - start_time) * 1000,
                2
            )

            response_body = response.text

            logger.info(
                "RESPONSE: %s %s",
                response.status_code,
                duration_ms
            )

            logger.info(
                "RESPONSE HEADERS: %s",
                json.dumps(
                    dict(response.headers),
                    default=str
                )
            )

            logger.info(
                "RESPONSE BODY: %s",
                response_body[:5000]
            )

            history_record = {
                "method": method.upper(),
                "url": url,
                "request": {
                    "headers": request_headers,
                    "params": request_params,
                    "body": request_body,
                    "form_data": request_data,
                    "files": file_metadata,
                },
                "response": {
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "body": response_body,
                },
                "duration_ms": duration_ms,
            }

            self.history.append(history_record)

            return response

        except requests.RequestException as exc:

            duration_ms = round(
                (time.perf_counter() - start_time) * 1000,
                2
            )

            logger.exception(
                "REQUEST FAILED: %s %s",
                method.upper(),
                url
            )

            self.history.append({
                "method": method.upper(),
                "url": url,
                "request": {
                    "headers": request_headers,
                    "params": request_params,
                    "body": request_body,
                    "form_data": request_data,
                    "files": file_metadata,
                },
                "error": str(exc),
                "duration_ms": duration_ms,
            })

            raise