from flask_login import UserMixin
from typing import Union, List
from abc import ABC, abstractmethod

# Abstract class for Users (Members, Trainers)
class User(ABC, UserMixin):
    id: str
    name: str
    membership_type: str  # e.g., Basic, Premium
    __password__: str

    def __repr__(self):
        return f'{self.id} - {self.name}'

# Abstract class for Classes
class Class(ABC):
    id: str
    name: str
    trainer_id: str  # Trainer assigned to the class
    schedule: str  # Schedule (e.g., '2025-04-07 09:00 AM')
    max_enrollment: int  # Max number of members allowed in the class

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
    
    @abstractmethod
    def get_user(self, user_id: str) -> Union[User, None]:
        pass
    
    @abstractmethod
    def create_user(self, user_id: str, name: str, membership_type: str, password: str) -> Union[User, None]:
        pass

    @abstractmethod
    def get_class(self, class_id: str) -> Union[Class, None]:
        pass

    @abstractmethod
    def create_class(self, name: str, trainer_id: str, schedule: str, max_enrollment: int) -> Union[Class, None]:
        pass

    @abstractmethod
    def enroll_member_in_class(self, user_id: str, class_id: str) -> bool:
        pass
    
    @abstractmethod
    def get_enrolled_members(self, class_id: str) -> List[User]:
        pass

    @abstractmethod
    def get_membership_plan(self, plan_id: str) -> Union[MembershipPlan, None]:
        pass
    
    @abstractmethod
    def assign_trainer_to_class(self, trainer_id: str, class_id: str) -> bool:
        pass

    @abstractmethod
    def create_membership_plan(self, type: str, duration: int, cost: float) -> Union[MembershipPlan, None]:
        pass
