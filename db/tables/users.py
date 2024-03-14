from sqlalchemy import Column, PrimaryKeyConstraint, String, Table, UUID, Enum
import sqlalchemy
from base import metadata
from models.user import UserRole

users = Table(
    'users',
    metadata,
    Column('id', UUID, nullable=False, server_default=sqlalchemy.text('gen_random_uuid()')),
    Column('name', String, nullable=False),
    Column('login', String, nullable=False),
    Column('password', String, nullable=False),
    Column('role', Enum(UserRole), nullable=False),
    PrimaryKeyConstraint('id', name='user_pk'),
)
