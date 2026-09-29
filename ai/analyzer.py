import json
import logging
from typing import Any

from transformers import pipeline

from config.settings import AI_MODEL_NAME

logger = logging.getLogger(__name__)


class ApiResponseAnalyzer:

    def __init__(self) -> None:

        logger.info(
            "Loading Hugging Face model: %s",
            AI_MODEL_NAME
        )

        self.classifier = pipeline(
            "zero-shot-classification",
            model=AI_MODEL_NAME
        )

        logger.info(
            "Hugging Face model loaded successfully"
        )

    # ============================================================
    # EXPECTED API RESPONSE CATEGORY
    # ============================================================

    @staticmethod
    def get_expected_category(
        status_code: int
    ) -> str:

        if 200 <= status_code < 300:
            return "successful API response"

        if status_code == 400:
            return "validation error"

        if status_code == 401 or status_code == 403:
            return "authorization error"

        if status_code == 404:
            return "not found error"

        if 500 <= status_code < 600:
            return "server error"

        return "unexpected API response"

    # ============================================================
    # AI ANALYSIS
    # ============================================================

    def analyze(
        self,
        status_code: int,
        response_body: Any
    ) -> dict[str, Any]:

        if not isinstance(response_body, str):

            response_body = json.dumps(
                response_body,
                default=str
            )

        response_body = response_body[:3000]

        expected_category = self.get_expected_category(
            status_code
        )

        text = (
            f"HTTP status code: {status_code}\n"
            f"Expected API category: {expected_category}\n"
            f"API response:\n{response_body}"
        )

        candidate_labels = [
            "successful API response",
            "not found error",
            "validation error",
            "server error",
            "authorization error",
            "unexpected API response"
        ]

        logger.info(
            "Running AI analysis for HTTP status: %s",
            status_code
        )

        result = self.classifier(
            text,
            candidate_labels=candidate_labels
        )

        classification = result["labels"][0]

        confidence = round(
            float(result["scores"][0]),
            4
        )

        classification_match = (
            classification == expected_category
        )

        analysis = {
            "model": AI_MODEL_NAME,
            "status_code": status_code,
            "expected_category": expected_category,
            "classification": classification,
            "confidence": confidence,
            "classification_match": classification_match,
            "all_scores": {
                label: round(float(score), 4)
                for label, score in zip(
                    result["labels"],
                    result["scores"]
                )
            }
        }

        logger.info(
            "Expected category: %s",
            expected_category
        )

        logger.info(
            "AI classification: %s",
            classification
        )

        logger.info(
            "AI confidence: %s",
            confidence
        )

        logger.info(
            "AI classification matches expected category: %s",
            classification_match
        )

        return analysis