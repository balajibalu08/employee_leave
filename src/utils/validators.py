from utils.config import config
from utils.logger import logger


def validate_employee_id(employee_id: int) -> bool:
    """
    Validate employee ID.
    """

    length = len(str(employee_id))

    if employee_id <= 0:
        logger.warning(f"Employee ID {employee_id} must be greater than zero.")
        return False

    if length < config["validations"]["min_length_of_employee_id"]:
        logger.warning(
            f"Employee ID {employee_id} must have at least "
            f"{config['validations']['min_length_of_employee_id']} digits."
        )
        return False

    if length > config["validations"]["max_length_of_employee_id"]:
        logger.warning(
            f"Employee ID {employee_id} must not exceed "
            f"{config['validations']['max_length_of_employee_id']} digits."
        )
        return False

    logger.info(f"Employee ID {employee_id} validation successful.")
    return True


def validate_employee_name(employee_name: str) -> bool:
    """
    Validate employee Name.
    """

    length = len(employee_name.strip())
    words = list(employee_name.split())
    if not all(word.isalpha() for word in words):
        logger.warning(f"Employee Name {employee_name} must be In Characters.")
        return False

    if length < config["validations"]["min_length_of_employee_name"]:
        logger.warning(
            f"Employee Name {employee_name} must have at least "
            f"{config['validations']['min_length_of_employee_name']} Characters."
        )
        return False

    if length > config["validations"]["max_length_of_employee_name"]:
        logger.warning(
            f"Employee Name {employee_name} must not exceed "
            f"{config['validations']['max_length_of_employee_name']} Characters."
        )
        return False

    logger.info(f"Employee Name {employee_name} validation successful.")
    return True


def validate_leave_days(leave_days: int) -> bool:
    if leave_days <= 0:
        logger.warning(f"leave Days {leave_days} Can't be 0 or less than Zero")
        return False
    logger.info(f"leave Days {leave_days} Validation sucessful.")
    return True


def validate_leave_balance(requested_leave: int, available_leave: int) -> bool:
    if not validate_leave_days(requested_leave):
        logger.warning(f"requested_leave {requested_leave} should be integer")
        return False
    if not validate_leave_days(available_leave):
        logger.warning(f"available_leave {available_leave} should be integer")
        return False
    if available_leave < requested_leave:
        logger.warning(
            f"Available_leave {available_leave} should be greather than or equal to Requested leave {requested_leave}"
        )
        return False
    logger.info(
        f"Validating requested_leave: {requested_leave} available_leave: {available_leave} Leave balance is sucessfull."
    )
    return True


def employee_exists(employee_id: int, employees: list[dict]) -> bool:
    for emp in employees:
        if emp["employee_id"] == employee_id:
            logger.info(f"Employee {employee_id} exist.")
            return True
    logger.warning(f"Employee {employee_id} not exist.")
    return False
