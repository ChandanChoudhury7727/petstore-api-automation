import json
from typing import Any

import allure


# ============================================================
# JSON ATTACHMENT
# ============================================================

def attach_json(name: str, data: Any) -> None:
    allure.attach(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
            default=str
        ),
        name=name,
        attachment_type=allure.attachment_type.JSON
    )


# ============================================================
# TEXT ATTACHMENT
# ============================================================

def attach_text(name: str, data: str) -> None:
    allure.attach(
        data,
        name=name,
        attachment_type=allure.attachment_type.TEXT
    )


# ============================================================
# SENSITIVE HEADER REDACTION
# ============================================================

def redact_headers(headers: Any) -> Any:
    """
    Hide sensitive header values before attaching them
    to the Allure report.
    """

    if not isinstance(headers, dict):
        return headers

    sensitive_headers = {
        "authorization",
        "proxy-authorization",
        "cookie",
        "set-cookie",
        "x-api-key"
    }

    safe_headers = {}

    for key, value in headers.items():

        if str(key).lower() in sensitive_headers:
            safe_headers[key] = "[REDACTED]"
        else:
            safe_headers[key] = value

    return safe_headers


# ============================================================
# API HISTORY ATTACHMENTS
# ============================================================

def attach_api_history(
    history: list[dict[str, Any]]
) -> None:
    """
    Attach API execution history to Allure.

    Adds:
      1. Combined API Request Response History
      2. Individual request and response attachments
    """

    if not history:
        return

    # --------------------------------------------------------
    # Attach combined history
    # --------------------------------------------------------

    safe_history = []

    for entry in history:

        safe_entry = dict(entry)

        request_data = safe_entry.get("request")

        if isinstance(request_data, dict):
            request_data = dict(request_data)

            request_data["headers"] = redact_headers(
                request_data.get("headers", {})
            )

            safe_entry["request"] = request_data

        response_data = safe_entry.get("response")

        if isinstance(response_data, dict):
            response_data = dict(response_data)

            response_data["headers"] = redact_headers(
                response_data.get("headers", {})
            )

            safe_entry["response"] = response_data

        safe_history.append(safe_entry)

    attach_json(
        "API Request Response History",
        safe_history
    )

    # --------------------------------------------------------
    # Attach each API interaction separately
    # --------------------------------------------------------

    for index, entry in enumerate(safe_history, start=1):

        method = entry.get("method", "UNKNOWN")
        url = entry.get("url", "UNKNOWN")

        request_data = entry.get("request", {})
        response_data = entry.get("response", {})

        duration_ms = entry.get("duration_ms")

        # ----------------------------------------------------
        # Request details
        # ----------------------------------------------------

        request_attachment = {
            "method": method,
            "url": url,
            "headers": request_data.get("headers", {}),
            "params": request_data.get("params"),
            "body": request_data.get("body"),
            "form_data": request_data.get("form_data"),
            "files": request_data.get("files")
        }

        attach_json(
            f"API Request {index} - {method} {url}",
            request_attachment
        )

        # ----------------------------------------------------
        # Response details
        # ----------------------------------------------------

        response_attachment = {
            "method": method,
            "url": url,
            "status_code": response_data.get("status_code"),
            "headers": response_data.get("headers", {}),
            "body": response_data.get("body"),
            "duration_ms": duration_ms
        }

        attach_json(
            f"API Response {index} - {method} {url}",
            response_attachment
        )

    attach_api_timing_summary(safe_history)

# ============================================================
# HUGGING FACE AI ANALYSIS ATTACHMENT
# ============================================================

def attach_ai_analysis(
    analyzer,
    status_code: int,
    response_body,
    expected_category: str | None = None
) -> dict[str, Any]:
    """
    Analyze an API response using Hugging Face and attach
    a structured result to Allure.
    """

    analysis = analyzer.analyze(
        status_code=status_code,
        response_body=response_body
    )

    actual_category = analysis.get("classification")

    match_status = None

    if expected_category is not None:
        match_status = actual_category == expected_category

    report = {
        "model": analysis.get("model"),
        "http_status_code": status_code,
        "expected_category": expected_category,
        "actual_category": actual_category,
        "confidence": analysis.get("confidence"),
        "classification_matches_expected": match_status,
        "all_scores": analysis.get("all_scores")
    }

    attach_json(
        "Hugging Face AI Analysis",
        report
    )

    return report

# ============================================================
# API EXECUTION-TIME SUMMARY
# ============================================================

def attach_api_timing_summary(
    history: list[dict[str, Any]]
) -> None:
    """
    Calculate and attach API execution-time statistics
    to the Allure report.

    Uses duration_ms recorded by BaseApiClient.
    """

    if not history:
        return

    timing_records = []

    for entry in history:

        duration_ms = entry.get("duration_ms")

        # Skip entries without a valid duration.
        if not isinstance(duration_ms, (int, float)):
            continue

        method = entry.get("method", "UNKNOWN")
        url = entry.get("url", "UNKNOWN")

        timing_records.append({
            "method": method,
            "url": url,
            "duration_ms": round(float(duration_ms), 2)
        })

    if not timing_records:
        return

    durations = [
        record["duration_ms"]
        for record in timing_records
    ]

    total_duration = sum(durations)

    summary = {
        "total_api_requests": len(timing_records),

        "total_api_duration_ms": round(
            total_duration,
            2
        ),

        "average_api_duration_ms": round(
            total_duration / len(durations),
            2
        ),

        "fastest_request_ms": round(
            min(durations),
            2
        ),

        "slowest_request_ms": round(
            max(durations),
            2
        ),

        "requests": timing_records
    }

    attach_json(
        "API Execution Time Summary",
        summary
    )
