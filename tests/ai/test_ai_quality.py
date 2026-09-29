import pytest
import allure

from utils.allure_helper import attach_json


@pytest.mark.parametrize(
    "status_code,response_body,expected_category",
    [
        (
            200,
            {
                "id": 12345,
                "name": "TestPet",
                "status": "available"
            },
            "successful API response"
        ),
        (
            400,
            {
                "code": 400,
                "type": "error",
                "message": "Invalid request"
            },
            "validation error"
        ),
        (
            401,
            {
                "code": 401,
                "type": "error",
                "message": "Unauthorized"
            },
            "authorization error"
        ),
        (
            403,
            {
                "code": 403,
                "type": "error",
                "message": "Forbidden"
            },
            "authorization error"
        ),
        (
            404,
            {
                "code": 404,
                "type": "error",
                "message": "Pet not found"
            },
            "not found error"
        ),
        (
            500,
            {
                "code": 500,
                "type": "error",
                "message": "Internal server error"
            },
            "server error"
        )
    ]
)
@allure.epic("Swagger Petstore API")
@allure.feature("AI-Powered API Analysis")
@allure.story("Hugging Face AI Quality Evaluation")
@allure.severity(allure.severity_level.NORMAL)
def test_ai_classification_quality(
    ai_analyzer,
    status_code,
    response_body,
    expected_category
):

    allure.dynamic.parameter(
        "HTTP Status",
        str(status_code)
    )

    allure.dynamic.parameter(
        "Expected Category",
        expected_category
    )

    with allure.step(
        f"Analyze HTTP {status_code} response"
    ):

        analysis = ai_analyzer.analyze(
            status_code=status_code,
            response_body=response_body
        )

    attach_json(
        "AI Quality Analysis",
        analysis
    )

    assert analysis["status_code"] == status_code

    assert (
        analysis["expected_category"]
        == expected_category
    )

    assert analysis["classification"]

    assert 0 <= analysis["confidence"] <= 1
    
@allure.epic("Swagger Petstore API")
@allure.feature("AI-Powered API Analysis")
@allure.story("Hugging Face AI Evaluation Summary")
@allure.severity(allure.severity_level.NORMAL)
def test_ai_evaluation_summary(ai_analyzer):

    scenarios = [
        (
            200,
            {
                "id": 12345,
                "name": "TestPet",
                "status": "available"
            },
            "successful API response"
        ),
        (
            400,
            {
                "code": 400,
                "type": "error",
                "message": "Invalid request"
            },
            "validation error"
        ),
        (
            401,
            {
                "code": 401,
                "type": "error",
                "message": "Unauthorized"
            },
            "authorization error"
        ),
        (
            403,
            {
                "code": 403,
                "type": "error",
                "message": "Forbidden"
            },
            "authorization error"
        ),
        (
            404,
            {
                "code": 404,
                "type": "error",
                "message": "Pet not found"
            },
            "not found error"
        ),
        (
            500,
            {
                "code": 500,
                "type": "error",
                "message": "Internal server error"
            },
            "server error"
        )
    ]

    results = []

    for status_code, response_body, expected_category in scenarios:

        with allure.step(
            f"Analyze HTTP {status_code}"
        ):

            analysis = ai_analyzer.analyze(
                status_code=status_code,
                response_body=response_body
            )

        results.append({
            "status_code": status_code,
            "expected_category": expected_category,
            "classification": analysis["classification"],
            "confidence": analysis["confidence"],
            "classification_match": (
                analysis["classification"]
                == expected_category
            )
        })

    total_scenarios = len(results)

    correct_predictions = sum(
        result["classification_match"]
        for result in results
    )

    incorrect_predictions = (
        total_scenarios
        - correct_predictions
    )

    accuracy = round(
        correct_predictions / total_scenarios,
        4
    )

    summary = {
        "total_scenarios": total_scenarios,
        "correct_predictions": correct_predictions,
        "incorrect_predictions": incorrect_predictions,
        "accuracy": accuracy,
        "accuracy_percentage": round(
            accuracy * 100,
            2
        ),
        "results": results
    }

    attach_json(
        "AI Evaluation Summary",
        summary
    )

    assert total_scenarios == 6
    assert (
        correct_predictions
        + incorrect_predictions
        == total_scenarios
    )