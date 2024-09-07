import logging
import os


def setup_logging():
    """Sets up logging configurations."""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()  # Default to INFO if LOG_LEVEL is not set

    # Define log format based on log level
    if log_level == "DEBUG":
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    else:
        log_format = "%(message)s"

    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),  # Set the logging level from env variable
        format=log_format,
        handlers=[
            logging.StreamHandler(),  # Output logs to the console
        ],
        datefmt="%d/%m/%Y %H:%M:%S",
    )
