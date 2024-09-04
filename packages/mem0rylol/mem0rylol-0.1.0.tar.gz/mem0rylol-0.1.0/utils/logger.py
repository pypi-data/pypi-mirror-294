import os
from loguru import logger

# Get log level from environment variable, default to INFO
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Configure logger
logger.configure(
    handlers=[
        # Console handler
        {"sink": "logs/sys.stdout", "level": LOG_LEVEL},
        # File handler for all logs
        {"sink": "logs/app.log", "rotation": "500 MB", "level": LOG_LEVEL, "serialize": True},
        # File handler for errors
        {"sink": "logs/errors.log", "rotation": "100 MB", "level": "ERROR", "serialize": True},
    ]
)

# Add correlation ID to all log records
logger = logger.bind(correlation_id=None)

# Export the logger
__all__ = ["logger"]