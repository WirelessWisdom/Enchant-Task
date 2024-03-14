from enum import Enum

from pydantic import BaseModel


class UserRole(Enum):
    ADMIN = 'admin'
    USER = 'user'


class User(BaseModel):
    name: str
    login: str
    password: str
    role: UserRole
