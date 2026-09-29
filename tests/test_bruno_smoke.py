import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

import allure


PROJECT_ROOT = Path(__file__).resolve().parents[1]

BRUNO_COLLECTION = PROJECT_ROOT / "bruno" / "petstore-smoke"
BRUNO_ENV = BRUNO_COLLECTION / "environments" / "Environment 1.yml"
BRUNO_REPORT = BRUNO_COLLECTION / "reports" / "bruno-smoke-results.xml"

BRUNO_CMD = Path.home() / "AppData" / "Roaming" / "npm" / "bru.cmd"


def test_bruno_smoke_collection():
    """
    Execute Bruno smoke tests and validate the generated JUnit report.
    """

    # Verify Bruno CLI
    assert BRUNO_CMD.exists(), (
        f"Bruno CLI was not found at: {BRUNO_CMD}"
    )

    # Verify Bruno collection
    assert BRUNO_COLLECTION.exists(), (
        f"Bruno collection was not found at: {BRUNO_COLLECTION}"
    )

    # Verify environment file
    assert BRUNO_ENV.exists(), (
        f"Bruno environment file was not found at: {BRUNO_ENV}"
    )

    # Create report directory
    BRUNO_REPORT.parent.mkdir(parents=True, exist_ok=True)

    # Execute Bruno directly through the .cmd launcher.
    # shell=True allows Windows to execute the .cmd file correctly.
    result = subprocess.run(
        [
            str(BRUNO_CMD),
            "run",
            "smoke-tests",
            "--env-file",
            str(BRUNO_ENV),
            "--reporter-junit",
            str(BRUNO_REPORT),
        ],
        cwd=BRUNO_COLLECTION,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
        shell=True,
    )

    allure.attach(
        result.stdout,
        name="Bruno Execution Output",
        attachment_type=allure.attachment_type.TEXT,
    )

    if result.stderr:
        allure.attach(
            result.stderr,
            name="Bruno Error Output",
            attachment_type=allure.attachment_type.TEXT,
        )

    # Validate Bruno execution
    assert result.returncode == 0, (
        "Bruno execution failed.\n\n"
        f"STDOUT:\n{result.stdout}\n\n"
        f"STDERR:\n{result.stderr}"
    )

    # Validate JUnit report
    assert BRUNO_REPORT.exists(), (
        f"Bruno JUnit report was not generated: {BRUNO_REPORT}"
    )

    allure.attach.file(
        str(BRUNO_REPORT),
        name="Bruno JUnit Report",
        attachment_type=allure.attachment_type.XML,
    )

    # Parse JUnit XML
    root = ET.parse(BRUNO_REPORT).getroot()

    if root.tag == "testsuite":
        suites = [root]
    else:
        suites = root.findall(".//testsuite")

    assert suites, (
        "No test suites were found in the Bruno JUnit report."
    )

    # Calculate test results
    total_tests = sum(
        int(suite.get("tests", 0))
        for suite in suites
    )

    failures = sum(
        int(suite.get("failures", 0))
        for suite in suites
    )

    errors = sum(
        int(suite.get("errors", 0))
        for suite in suites
    )

    # Validate results
    assert total_tests > 0, (
        "Bruno did not execute any tests."
    )

    assert failures == 0, (
        f"Bruno reported {failures} failure(s)."
    )

    assert errors == 0, (
        f"Bruno reported {errors} error(s)."
    )