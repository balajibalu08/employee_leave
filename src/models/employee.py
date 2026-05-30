from __future__ import annotations


class Employee:
    def __init__(
        self, employee_id: int, employee_name: str, leave_balance: int
    ) -> None:
        self.employee_id = employee_id
        self.employee_name = employee_name
        self.leave_balance = leave_balance

    def to_dict(self) -> dict:
        """
        Converts the object to Dict
        """
        employee = {}
        employee["employee_id"] = self.employee_id
        employee["employee_name"] = self.employee_name
        employee["leave_balance"] = self.leave_balance
        return employee

    @classmethod
    def from_dict(cls, data: dict) -> Employee:
        """
        Converts the Dict to object
        """
        return cls(data["employee_id"], data["employee_name"], data["leave_balance"])

    def __str__(self):
        return f"\nEmployee_id : {self.employee_id} \nEmployee_name : {self.employee_name} \nleave_balance : {self.leave_balance}"
