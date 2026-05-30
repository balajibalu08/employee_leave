import json
from src.utils.logger import logger
#Reads JSON
def read_json(file_path:str)-> list[dict]:
    """
        Read data from a JSON file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"Successfully loaded JSON file: {file_path}")
        return data
    except FileNotFoundError:
        logger.error(f"JSON file not found: {file_path}")
        raise

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format in {file_path}: {e}")
        raise

    except Exception:
        logger.exception(f"Unexpected error while reading {file_path}")
        raise

#Write JSON
def write_json(file_path:str, data:list[dict])-> None:
    """
    Write data to a JSON file.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
            logger.info(
                f"Successfully wrote data to JSON file: {file_path}"
            )
    except PermissionError:
        logger.error(
            f"Permission denied while writing to file: {file_path}"
        )
        raise
    except Exception:
        logger.exception(
            f"Unexpected error while writing to {file_path}"
        )
        raise