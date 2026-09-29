import logging
from pathlib import Path


# ============================================================
# LOG DIRECTORY
# ============================================================

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "test_execution.log"


# ============================================================
# LOGGING CONFIGURATION
# ============================================================

def configure_logging() -> None:
    """
    Configure application-wide logging.

    Logs are written to:
    1. Console
    2. logs/test_execution.log
    """

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        handlers=[
            logging.FileHandler(
                LOG_FILE,
                encoding="utf-8"
            ),
            logging.StreamHandler()
        ],
        force=True
    )