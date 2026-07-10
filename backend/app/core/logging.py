import logging


def configure_logging(environment: str) -> None:
    log_level = logging.DEBUG if environment == "development" else logging.INFO

    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
