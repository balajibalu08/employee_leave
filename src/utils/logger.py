import config
import logging

# Logging basic Configuration
logging.basicConfig(
    filename=config["logging"]["file"],
    level=config["logging"]["level"],
    format=config["logging"]["format"],
)
