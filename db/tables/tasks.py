from sqlalchemy import Column, PrimaryKeyConstraint, String, Table, UUID, Enum, DateTime, ForeignKey
import sqlalchemy
from models import TaskStatus
from base import metadata

tasks = Table(
    'tasks',
    metadata,
    Column('id', UUID, nullable=False, server_default=sqlalchemy.text('gen_random_uuid()')),
    Column('name', String, nullable=False),
    Column('description', String, nullable=True),
    Column('status', Enum(TaskStatus), nullable=False),
    Column('created_at', DateTime, nullable=False),
    Column('due_date', DateTime, nullable=True),
    Column('created_by', String, ForeignKey('users.id'), nullable=False),
    Column('assignee', String, ForeignKey('users.id'), nullable=True),
    PrimaryKeyConstraint('id', name='task_pk'),

)