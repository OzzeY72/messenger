import sys
import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context

if context.config.config_file_name is not None:
    fileConfig(context.config.config_file_name)

from app.database import Base, DATABASE_URL
from app.users import models 

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migration in offline"""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migration in async"""
    connectable = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
        future=True,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
