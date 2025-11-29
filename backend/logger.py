import logging 
import os
from logging.handlers import RotatingFileHandler

# Create logs directory 
os.makedirs("logs", exist_ok=True)

# configure logger
logger = logging.getLogger("college_management")
logger.setLevel(logging.INFO)

# file handler with rotation
file_handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=10485760,
    backupCount=5
)
file_handler.setLevel(logging.INFO)

# console handler 
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
