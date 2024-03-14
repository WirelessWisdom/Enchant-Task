from sqlalchemy import Column, PrimaryKeyConstraint, String, Table, UUID
from base import metadata

users = Table(
    'users',
    metadata,
    Column('id', UUID, nullable=False),
    Column('name', String, nullable=False),
    Column('login', String, nullable=False),
    Column('password', String, nullable=False),
    Column('role', String, nullable=False),
    PrimaryKeyConstraint('id', name='user_pk'),
)
