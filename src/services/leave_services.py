from utils.config import config
from utils.logger import logger
from utils.validators import (
    validate_employee_id,
    validate_employee_name,
    validate_leave_balance,
    validate_leave_days,
    employee_exists,
)
from models.employee import Employee
from models.leave import Leave
from datetime import date
from storage.json_storage import read_json, write_json


def add_employee(employee_id: int, employee_name: str) -> bool:
    """
    Add a new employee to the system.
    """
    if not validate_employee_id(employee_id=employee_id):
        return False
    if not validate_employee_name(employee_name=employee_name):
        return False
    try:
        employees = read_json(config["Storage"]["employee_data"])
        if employee_exists(employee_id=employee_id):
            return False
        employee = Employee(
            employee_id=employee_id,
            employee_name=employee_name,
            leave_balance=config["policy"]["annual_leaves"],
        )
        logger.info(
            f"Employee {employee.employee_id} is created Sucessfully with given bellow details \n Employee_id: {employee_id} Employee_name : {employee_name}"
        )
        employee_json = employee.to_dict()
        employees.append(employee_json)
        logger.info(f"Employee {employee.employee_id} added to Employee List")
        write_json(config["Storage"]["employee_data"], data=employees)
        logger.info("Employees wrtien to json file")
        return True
    except Exception as e:
        logger.error(
            f"Employee is not created with given bellow details \n Employee_id: {employee_id} Employee_name : {employee_name} for given error : {e}"
        )
        return False


def apply_leave(
    employee_id: int, leave_days: int, reason: str, applied_date: date
) -> bool:
    """
    Add a new Leave history to the system.
    """
    try:
        employees = read_json(config["Storage"]["employee_data"])
        if not employee_exists(employee_id):
            return False
        if not validate_leave_days(leave_days=leave_days):
            return False
        leave = Leave(
            employee_id=employee_id,
            leave_days=leave_days,
            reason=reason,
            applied_date=applied_date,
        )
        logger.info(f"Leave record created for employee_id : {leave.employee_id}")
        leaves = read_json(config["Storage"]["leave_history"])
        leave_json = leave.to_dict()
        for emp in employees:
            if employee_id == emp["employee_id"]:
                if validate_leave_balance(
                    requested_leave=leave_days, available_leave=emp["leave_balance"]
                ):
                    emp["leave_balance"] -= leave_days
                    leaves.append(leave_json)
                    logger.info(
                        f"Leave balance has been updated for employee_id: {emp['employee_id']}"
                    )
                else:
                    logger.warning(
                        f"Employee {emp['employee_id']}Leaves has Less than requested"
                    )
                    return False

        write_json(config["Storage"]["employee_data"], employees)
        logger.info("Employee Details Updated")
        write_json(config["Storage"]["leave_history"], leaves)
        logger.info("Leave History Updated")
        return True
    except Exception as e:
        logger.error(f"Got UnExpected Error {e}")
        raise


def view_balance(employee_id: int) -> int | None:
    try:
        employees = read_json(config["Storage"]["employee_data"])
        if not employee_exists(employee_id=employee_id):
            return None

        for emp in employees:
            if emp["employee_id"] == employee_id:
                logger.info(
                    f"Employee {employee_id} leave balance successfully retrieved."
                )
                return emp["leave_balance"]
    except Exception:
        logger.exception(f"Failed to Retrieve balence for employee_id {employee_id}")
        raise


def view_leave_history(employee_id: int) -> list[Leave]:
    try:
        if not employee_exists(employee_id=employee_id):
            logger.warning(f"No Such employee {employee_id} found")
            return []
        leaves = read_json(config["Storage"]["leave_history"])
        employee_leaves = []
        for leave in leaves:
            if leave["employee_id"] == employee_id:
                employee_leaves.append(Leave.from_dict(leave))
        logger.info(
            f"Retrieved {len(employee_leaves)} leave records for employee_id={employee_id}"
        )
        return employee_leaves
    except Exception:
        logger.exception(f"Failed to Retrieve leaves for employee_id {employee_id}")
        raise


def list_employees() -> list[Employee]:
    try:
        employees_json = read_json(config["Storage"]["employee_data"])
        employees = []
        for employee in employees_json:
            employees.append(Employee.from_dict(employee))
        logger.info(f"Retrieved {len(employees)} Employee Records")
        return employees
    except Exception:
        logger.exception("Failed to Retrieve list of  employees")
        raise


def get_employee_id() -> int:
    while True:
        try:
            employee_id = int(input("Enter Employee ID (9-10 digits):"))
            if not validate_employee_id(employee_id):
                print("Invalid Employee ID")
                continue
            return employee_id
        except ValueError:
            print("Please enter a valid number.")
            logger.warning("User entered non-numeric Employee ID.")
