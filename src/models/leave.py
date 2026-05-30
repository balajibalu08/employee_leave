from __future__ import annotations
from datetime import date, datetime


class Leave:
    def __init__(
        self, employee_id: int, leave_days: int, reason: str, applied_date: date
    ) -> None:
        self.employee_id = employee_id
        self.leave_days = leave_days
        self.reason = reason
        self.applied_date = applied_date

    def to_dict(self) -> dict:
        """
        Converts the object to Dict
        """
        return {
            "employee_id": self.employee_id,
            "leave_days": self.leave_days,
            "reason": self.reason,
            "applied_date": self.applied_date.strftime("%Y-%m-%d"),
        }

    @classmethod
    def from_dict(cls, data: dict) -> Leave:
        """
        Converts the Dict to object
        """
        return cls(
            data["employee_id"],
            data["leave_days"],
            data["reason"],
            datetime.strptime(data["applied_date"], "%Y-%m-%d").date(),
        )

    def __str__(self) -> str:
        return f"Employee_id : {self.employee_id} \nleave_days : {self.leave_days} \nreason : {self.reason} \napplied_date : {self.applied_date}"
