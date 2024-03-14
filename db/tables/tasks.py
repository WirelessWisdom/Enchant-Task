from sqlalchemy import Column, PrimaryKeyConstraint, String, Table, UUID, Enum, DateTime
from models import TaskStatus
from base import metadata

tasks = Table(
    'tasks',
    metadata,
    Column('id', UUID, nullable=False),
    Column('name', String, nullable=False),
    Column('description', String, nullable=False),
    Column('status', Enum(TaskStatus), nullable=False),
    Column('created_at', DateTime, nullable=False),
    Column('due_date', DateTime, nullable=False),
    Column('user', String, nullable=False),
    PrimaryKeyConstraint('id', name='task_pk'),
)