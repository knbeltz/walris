# Logging configuration for the app.
#
# Pseudocode (Phase 3, Milestone 3):
#   2. Configure logging using values from settings
#
# TODO:
# - Write a function, e.g. configure_logging(environment: str) -> None,
#   that sets up Python's built-in `logging` module (e.g. via
#   logging.basicConfig) — more verbose in development, less verbose in
#   production.
# - This should be called once from main.py, after settings have loaded,
#   since it needs a value (environment) that only exists after step 1.

import logging

def configure_logging(environment: str) -> None:
    if environment == "development":
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )