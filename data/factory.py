import uuid
from typing import Any


def generate_unique_id() -> int:
    return (uuid.uuid4().int % 1_000_000_000) + 1


def generate_unique_name(prefix: str = "AutomationPet") -> str:
    unique_value = uuid.uuid4().hex[:10]
    return f"{prefix}-{unique_value}"


def generate_pet_payload() -> dict[str, Any]:
    unique_id = generate_unique_id()
    unique_name = generate_unique_name()

    return {
        "id": unique_id,
        "category": {
            "id": generate_unique_id(),
            "name": f"Category-{uuid.uuid4().hex[:8]}"
        },
        "name": unique_name,
        "photoUrls": [
            f"https://example.com/{uuid.uuid4().hex}.jpg"
        ],
        "tags": [
            {
                "id": generate_unique_id(),
                "name": f"automation-{uuid.uuid4().hex[:8]}"
            },
            {
                "id": generate_unique_id(),
                "name": f"test-{uuid.uuid4().hex[:8]}"
            }
        ],
        "status": "available"
    }