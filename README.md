Absolutely. Below is a **professional, GitHub-ready README** tailored to the project we've actually built. You can copy-paste the entire thing into your `README.md`.

````markdown
# Petstore API Automation Framework

A portfolio-grade API automation framework built using **Python, Pytest, Bruno, Allure, OpenAPI Schema Validation, and Hugging Face AI**.

The framework automates functional, negative, schema, CRUD, file-upload, and AI-assisted API testing against the **Swagger Petstore API**.

---

## 🚀 Project Overview

This project demonstrates a complete API testing workflow combining traditional Python-based automation with Bruno API testing.

The framework provides:

- Automated API testing using Pytest
- Dynamic test data generation
- Complete Pet CRUD lifecycle testing
- Positive and negative API testing
- File upload testing
- OpenAPI-based schema validation
- Hugging Face AI-based API response analysis
- Bruno API collection and smoke testing
- Dynamic Bruno CRUD workflow
- Allure test reporting
- JUnit reporting
- Centralized logging
- Reusable API client architecture

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Programming language |
| Pytest | Test automation framework |
| Requests | HTTP API communication |
| Bruno | API collection and smoke testing |
| Allure | Test reporting |
| Hugging Face | AI-based API response analysis |
| OpenAPI | API contract/schema validation |
| JSON Schema | Response validation |
| Git | Version control |
| GitHub | Source code repository |

---

## 🔗 API Under Test

**Swagger Petstore API**

Base URL:

```text
https://petstore.swagger.io/v2
````

OpenAPI specification:

```text
https://petstore.swagger.io/v2/swagger.json
```

---

# 📁 Project Structure

```text
Testing/
│
├── ai/
│   ├── __init__.py
│   └── analyzer.py
│
├── api/
│   ├── __init__.py
│   ├── base_client.py
│   └── pet_api.py
│
├── bruno/
│   └── petstore-smoke/
│       ├── environments/
│       ├── pet/
│       ├── store/
│       ├── user/
│       ├── reports/
│       ├── smoke-tests/
│       └── opencollection.yml
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── data/
│   ├── __init__.py
│   └── factory.py
│
├── schemas/
│   ├── __init__.py
│   ├── openapi_loader.py
│   └── response_validator.py
│
├── test_data/
│   └── images/
│       └── pet_test_image.png
│
├── tests/
│   ├── ai/
│   │   ├── test_ai_analysis.py
│   │   └── test_ai_quality.py
│   │
│   ├── pet/
│   │   ├── test_pet_crud.py
│   │   ├── test_pet_fetch.py
│   │   ├── test_pet_negative.py
│   │   ├── test_pet_schema.py
│   │   └── test_pet_upload.py
│   │
│   └── test_bruno_smoke.py
│
├── utils/
│   ├── __init__.py
│   ├── allure_helper.py
│   └── logger.py
│
├── conftest.py
├── pytest.ini
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ✨ Key Features

## 1. Pytest API Automation

The framework uses Pytest to automate API test scenarios with a reusable architecture.

The API layer separates HTTP communication from test cases, making the framework easier to maintain and extend.

---

## 2. Dynamic Test Data

Test data is generated dynamically instead of relying on fixed Pet IDs.

Example:

```text
UUID / dynamically generated identifiers
```

This reduces dependency on previously existing API data and allows tests to be executed repeatedly.

---

## 3. Pet CRUD Automation

The framework validates the complete Pet lifecycle:

```text
Create Pet
    ↓
Get Pet
    ↓
Update Pet
    ↓
Delete Pet
    ↓
Verify Deletion
```

The same concept is also implemented in the Bruno smoke-test collection.

---

## 4. Positive API Testing

The framework validates successful API operations such as:

* Create Pet
* Get Pet
* Update Pet
* Delete Pet
* Find Pets by status
* Find Pets by tags
* Upload Pet image

---

## 5. Negative Testing

Negative scenarios are included to validate API behavior when invalid or unexpected inputs are provided.

Examples include:

* Invalid Pet ID
* Non-existent Pet
* Invalid request scenarios
* Expected HTTP error responses

---

## 6. File Upload Testing

The framework validates the Pet image upload endpoint.

Test image:

```text
test_data/images/pet_test_image.png
```

The test validates the API response after uploading the image.

---

# 📋 OpenAPI / Schema Validation

The framework dynamically loads the Swagger/OpenAPI specification and validates API responses against the expected schema.

Components:

```text
schemas/
├── openapi_loader.py
└── response_validator.py
```

This provides contract-level validation in addition to functional API testing.

---

# 🤖 Hugging Face AI Integration

The project includes Hugging Face model integration for automated API response analysis.

The analyzer evaluates API responses and classifies them into meaningful categories.

The project uses:

```text
typeform/distilbert-base-uncased-mnli
```

The AI component is used as an additional analysis layer rather than replacing deterministic API assertions.

AI-related tests are located in:

```text
tests/ai/
├── test_ai_analysis.py
└── test_ai_quality.py
```

---

# 🟣 Bruno API Testing

Bruno is integrated into the project for collection-based API testing.

The OpenAPI specification was imported into Bruno and organized into:

```text
bruno/petstore-smoke/
├── pet/
├── store/
├── user/
└── smoke-tests/
```

The project also contains a dedicated dynamic CRUD smoke flow.

---

## Bruno Dynamic CRUD Flow

```text
Find Available Pets
        ↓
Create Pet
        ↓
Get Created Pet
        ↓
Update Created Pet
        ↓
Delete Created Pet
        ↓
Verify Pet Deleted
```

The Pet ID is dynamically generated during execution.

Example:

```text
Generated Pet ID: 418262095
```

The generated ID is then reused throughout the CRUD workflow.

---

# 🔄 Bruno + Pytest Integration

Bruno is executed from the Pytest framework using the Bruno CLI.

The integration:

1. Executes the Bruno collection.
2. Captures Bruno execution output.
3. Generates a JUnit report.
4. Validates the JUnit report.
5. Attaches execution information to Allure.
6. Fails the Pytest test if Bruno execution fails.

This provides a single automation entry point through Pytest.

---

# 📊 Allure Reporting

Allure is used to generate detailed test execution reports.

The report contains:

* Test results
* Test status
* Bruno execution output
* Bruno JUnit report
* API test information
* AI analysis information
* Execution details

Generate an Allure report using:

```powershell
allure generate allure-results -o allure-report
```

Open the generated report:

```powershell
allure open allure-report
```

---
Screenshots of the Allure report:
**Overview**
<img width="588" height="690" alt="image" src="https://github.com/user-attachments/assets/09efe51b-141b-4fa3-aa56-20c78d64900b" />
<img width="575" height="405" alt="image" src="https://github.com/user-attachments/assets/dd683e67-c92e-4a14-a856-67563ce0a427" />


**Test Pet CURD lifecycle**
<img width="580" height="801" alt="image" src="https://github.com/user-attachments/assets/93dad0b0-848b-4014-b648-9d3577dcd2b3" />
<img width="567" height="665" alt="image" src="https://github.com/user-attachments/assets/44943db7-00df-4c5b-b0e0-e7b03ed3810d" />
<img width="585" height="907" alt="image" src="https://github.com/user-attachments/assets/901f089e-0cef-4f95-ba74-9588d815c1a5" />



**Test Valid Pet Matches Schema**
<img width="585" height="627" alt="image" src="https://github.com/user-attachments/assets/2bf29dc5-5520-4496-ba2d-2cd057a93599" />
<img width="590" height="715" alt="image" src="https://github.com/user-attachments/assets/de7f726b-45a0-410b-9633-ea1647b01d9b" />


**Upload Pet Image**
<img width="585" height="887" alt="image" src="https://github.com/user-attachments/assets/225cd43d-ef98-4d55-809d-c70c99a58c8e" />


**Teat AI Quality** 
<img width="582" height="767" alt="image" src="https://github.com/user-attachments/assets/95633400-4e82-44da-ba88-ee815c1552f4" />
<img width="580" height="803" alt="image" src="https://github.com/user-attachments/assets/7c10a1e3-803c-4a51-8e6b-8d1fb72f9635" />


**Test Bruno Smoke collection**
<img width="588" height="758" alt="image" src="https://github.com/user-attachments/assets/6bffd9e8-aa48-472b-b050-8b3ca5d30757" />
<img width="590" height="762" alt="image" src="https://github.com/user-attachments/assets/9258b360-b9db-4dc7-9561-f5a9180d1824" />


**Negative Test**
<img width="582" height="926" alt="image" src="https://github.com/user-attachments/assets/9927bfa6-22b9-47a8-a3a8-a1aba5f77598" />

# 📝 Logging

The framework includes centralized logging.

Logs are written to:

```text
logs/test_execution.log
```

The API client captures information such as:

* HTTP method
* Request URL
* Request body
* Response status
* Response body
* Response timing
* Request/response history

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/ChandanChoudhury7727/petstore-api-automation.git
```

Navigate to the project:

```bash
cd petstore-api-automation
```

---

## 2. Create a Virtual Environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

# 🧪 Running Tests

Run the complete Pytest suite:

```powershell
pytest -v
```

Generate Allure results:

```powershell
pytest -v --alluredir=allure-results
```

Generate the Allure report:

```powershell
allure generate allure-results -o allure-report
```

Open the report:

```powershell
allure open allure-report
```

---

# 🟣 Running Bruno Tests

Navigate to the Bruno collection:

```powershell
cd bruno\petstore-smoke
```

Run the smoke tests:

```powershell
bru run smoke-tests --env-file ".\environments\Environment 1.yml"
```

Generate JUnit results:

```powershell
bru run smoke-tests --env-file ".\environments\Environment 1.yml" --reporter-junit ".\reports\bruno-smoke-results.xml"
```

---

# 🔍 Example Bruno Execution

A successful CRUD execution follows this flow:

```text
find-available-pets       (200 OK)
create-pet                (200 OK)
get-created-pet           (200 OK)
update-created-pet        (200 OK)
delete-created-pet        (200 OK)
verify-pet-deleted        (404 Not Found)
```

The final `404 Not Found` is expected because the test verifies that the Pet was successfully deleted.

The Bruno test assertions validate the expected response behavior.

---

# 🧩 Configuration

The primary API configuration is maintained centrally in:

```text
config/settings.py
```

This includes configuration such as:

```text
BASE_URL
OpenAPI URL
Request timeout
AI model configuration
```

Centralized configuration avoids unnecessary hard-coding throughout the test framework.

---

# 🏗️ Framework Architecture

```text
                ┌─────────────────────┐
                │     Test Cases      │
                │      Pytest         │
                └──────────┬──────────┘
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
      ┌──────────────┐           ┌──────────────┐
      │   API Layer  │           │    Bruno     │
      │              │           │   Collection │
      └──────┬───────┘           └──────┬───────┘
             │                          │
             └────────────┬─────────────┘
                          ▼
                 ┌────────────────┐
                 │ Swagger Petstore│
                 │      API        │
                 └────────┬───────┘
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
          Validation     AI        Reporting
          OpenAPI      Analysis      Allure
```

---

# 📈 Testing Approach

The framework follows multiple levels of API validation:

```text
Functional Testing
       +
Negative Testing
       +
CRUD Testing
       +
Schema Validation
       +
File Upload Testing
       +
AI-assisted Analysis
       +
Bruno Collection Testing
       +
Allure Reporting
```

This provides both deterministic automation and additional AI-assisted analysis.

---

# 🎯 Project Objectives

The main objectives of this project are:

* Build a reusable API automation framework.
* Automate REST API functional testing.
* Reduce hard-coded test dependencies.
* Validate API contracts using OpenAPI schemas.
* Integrate AI-assisted API response analysis.
* Demonstrate Bruno collection-based API testing.
* Integrate multiple testing approaches into a single framework.
* Generate detailed and traceable test reports.

---

# 👨‍💻 Author

**Chandan Choudhury**

GitHub:

[https://github.com/ChandanChoudhury7727](https://github.com/ChandanChoudhury7727)

---



The project currently includes:

* ✅ Pytest API automation
* ✅ Dynamic test data
* ✅ CRUD testing
* ✅ Negative testing
* ✅ File upload testing
* ✅ OpenAPI schema validation
* ✅ Hugging Face AI integration
* ✅ Bruno API collection
* ✅ Dynamic Bruno CRUD testing
* ✅ Pytest + Bruno integration
* ✅ JUnit reporting
* ✅ Allure reporting
* ✅ Centralized logging
* ✅ Git/GitHub version control

````


