"""
logging_setup.py - Centralized logger configuration for the 'my_logger' logger.

This module sets up a logger named 'my_logger' with the following configuration:
- Logging level is set to DEBUG, so all messages with levels DEBUG and above will be captured.
- A console handler is attached, which outputs logs to the console.
- Logs are formatted to include the timestamp, logger name, log level, and the message.

Usage:
--------
To use the configured logger in other modules, simply import the `logger` variable:

    from logging_setup import logger

Example:
--------
    from logging_setup import logger

    logger.info("This is an info message")
"""

import logging
from logging.handlers import RotatingFileHandler

# Create a rotating file handler


# Configure the logger
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

# format
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# logger.info("Hello from logging.py")
# Console handler to output logs to the console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)


# File handler to write logs to 'my_project.log' in the root folder
file_handler = RotatingFileHandler("my_project.log", maxBytes=100000)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
