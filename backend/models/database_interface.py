from flask_login import UserMixin
from typing import Union, List
from abc import ABC, abstractmethod

# Abstract base class for Users
class User(ABC, UserMixin):
    id: str
    name: str
    membership_type: str  # e.g., Basic, Premium
    _password: str

    def __repr__(self):
        return f'{self.id} - {self.name}'

# Concrete Member class
class Member(User):
    contact_info: str
    join_date: str  # ISO date format e.g., "2025-04-10"

# Concrete Trainer class
class Trainer(User):
    specialization: str

# Abstract class for Classes
class Class(ABC):
    id: str
    name: str
    trainer_id: str
    schedule: str  # e.g., '2025-04-07 09:00 AM'
    max_enrollment: int

    def __repr__(self):
        return f'{self.id} - {self.name}'

# Abstract class for Membership Plans
class MembershipPlan(ABC):
    id: str
    type: str  # e.g., Basic, Premium
    duration: int  # Duration in months
    cost: float

    def __repr__(self):
        return f'{self.id} - {self.type}'

# Abstract class for database interaction
class Database(ABC):

    # ---------------- User Operations ----------------
    @abstractmethod
    def get_user(self, user_id: str) -> Union[User, None]:
        pass

    @abstractmethod
    def create_member(self, user_id: str, name: str, contact_info: str, membership_type: str, join_date: str, password: str) -> Union[Member, None]:
        pass

    @abstractmethod
    def create_trainer(self, user_id: str, name: str, specialization: str, password: str) -> Union[Trainer, None]:
        pass

    @abstractmethod
    def get_member(self, member_id: str) -> Union[Member, None]:
        pass

    @abstractmethod
    def get_trainer(self, trainer_id: str) -> Union[Trainer, None]:
        pass

    # ---------------- Class Operations ----------------
    @abstractmethod
    def get_class(self, class_id: str) -> Union[Class, None]:
        pass

    @abstractmethod
    def create_class(self, name: str, trainer_id: str, schedule: str, max_enrollment: int) -> Union[Class, None]:
        pass

    @abstractmethod
    def assign_trainer_to_class(self, trainer_id: str, class_id: str) -> bool:
        pass

    # ---------------- Enrollment Operations ----------------
    @abstractmethod
    def enroll_member_in_class(self, member_id: str, class_id: str) -> bool:
        pass

    @abstractmethod
    def get_enrolled_members(self, class_id: str) -> List[Member]:
        pass

    @abstractmethod
    def is_class_full(self, class_id: str) -> bool:
        pass

    # ---------------- Membership Plan Operations ----------------
    @abstractmethod
    def get_membership_plan(self, plan_id: str) -> Union[MembershipPlan, None]:
        pass

    @abstractmethod
    def create_membership_plan(self, type: str, duration: int, cost: float) -> Union[MembershipPlan, None]:
        pass
