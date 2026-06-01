from utils.config import config
from utils.logger import logger
from utils.validators import validate_employee_name, validate_leave_days
from services.leave_services import (
    add_employee,
    apply_leave,
    view_balance,
    get_employee_id,
    view_leave_history,
    list_employees,
)
from datetime import datetime


def menu():
    try:
        print(config["CLI"]["menu"])
        choice = int(input("Enter Choice (1-6): "))
        logger.info(f"User have selected {choice} option.")
    except ValueError:
        print("please Enter a valid number")
        logger.info("User entered a non-numeric menu choice.")
        return
    match choice:
        case 1:
            employee_id = get_employee_id()
            employee_name = input("Enter employee Name: ")
            while not validate_employee_name(employee_name=employee_name):
                print(
                    "Please Enter Valid Employee Name it have to be only characters no spl characters allowed and less than ",
                    config["validations"]["max_length_of_employee_name"],
                )
                employee_name = input("Enter employee Name: ")
            in_list = add_employee(employee_id=employee_id, employee_name=employee_name)
            if in_list:
                print(f"Employee added Successfully with employee id {employee_id}")
                logger.info(f"Employee {employee_id} added successfully.")
            else:
                print("Failed to add employee.")
        case 2:
            employee_id = get_employee_id()
            while True:
                try:
                    leave_days = int(input("Enter no.of Days Leaves Needed :"))

                    if validate_leave_days(leave_days):
                        break

                    print("Please enter valid leave days.")

                except ValueError:
                    print("Please enter a valid number.")
                    logger.warning("User entered non-numeric leave days.")
            while True:
                reason = input("Please Enter The Reason For Leave :").strip()

                if reason:
                    break

                print("Reason cannot be empty.")
            while True:
                user_input = input("Enter applied date (DD/MM/YYYY): ").strip()
                try:
                    # Attempt to parse the date
                    applied_date = datetime.strptime(user_input, "%d/%m/%Y").date()
                    # Break the loop if parsing succeeds
                    break
                except ValueError:
                    print(
                        "❌ Invalid date format. Please use DD/MM/YYYY (e.g., 25/12/2026).\n"
                    )
            logger.info(f"User selected leave application for employee {employee_id}")
            print("\nSubmitting leave request...")
            try:
                applied = apply_leave(
                    employee_id=employee_id,
                    leave_days=leave_days,
                    reason=reason,
                    applied_date=applied_date,
                )
                if applied:
                    print("Leave request Raised Successfully")
                    logger.info(
                        f"Employee {employee_id} Leave request Raised Successfully."
                    )
                else:
                    print("Failed to Raise Leave Request.")
            except Exception:
                print("An unexpected error occurred.")

        case 3:
            employee_id = get_employee_id()
            try:
                balance = view_balance(employee_id=employee_id)
                if balance is None:
                    print(f"Employee {employee_id} not found.")
                    logger.info(f"User Entered Employee {employee_id} not found")
                else:
                    print(f"Employee {employee_id} leave balance is {balance}")
                    logger.info(f"Employee {employee_id} retrieved leave balance")

            except Exception:
                print("An unexpected error occurred.")
                logger.exception(
                    f"Failed to retrieve balance for employee {employee_id}"
                )
        case 4:
            employee_id = get_employee_id()
            try:
                leaves = view_leave_history(employee_id=employee_id)
            except Exception:
                print("Failed to retrieve Leave History")
            if not leaves:
                print(f"No leave history found for employee {employee_id}")
                logger.warning(f"No leave history found for employee {employee_id}")
            else:
                logger.info(f"Fetched Leave History of Employee {employee_id}")
            print(f"\nLeave History of Employee {employee_id}")
            for leave in leaves:
                print(leave)
        case 5:
            employees = list_employees()
            if not employees:
                print("No employees found")
            else:  
                print("All the employees in Company is : \n")
                for employee in employees:
                    print(employee)
        case 6:
            logger.info("Application closed by user.")
            print("Thank you for using Leave Management System.")
            raise SystemExit
        case _:
            print("Invalid Choice. Please select between 1 and 6.")
            logger.info(f"User Entered Invalid Choice {choice}")


if __name__ == "__main__":
    while True:
        menu()
