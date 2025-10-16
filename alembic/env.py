import os
import sys
from logging.config import fileConfig

from sqlalchemy import create_engine, pool

from alembic import context

alembic_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(alembic_dir, '..')
sys.path.insert(0, project_root)

from dotenv import load_dotenv
from database.base import Base
from database.telegram import (
    BotChatHistory,
    BotUserMapping,
    BotUserSummary
)

load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
# config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata
for table_name in target_metadata.tables:
    print(f"- {table_name}")

# DATABASE_HOST = os.getenv("PI5_POSTGRES_DB_HOST", "localhost")
DATABASE_HOST = "localhost"
DATABASE_USER = os.getenv("PI5_POSTGRES_DB_USER", "postgres")
DATABASE_PWD = os.getenv("PI5_POSTGRES_DB_PWD", "password")
DATABASE_PORT = os.getenv("PI5_POSTGRES_DB_PORT", "5432")
DATABASE_NAME = os.getenv("PI5_POSTGRES_DB_NAME", "postgres")
DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PWD}@\
{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def include_object(object, name, type_, reflected, compare_to):
    """
    Kembalikan True jika objek harus disertakan dalam autogenerate,
    False jika harus diabaikan.
    """
    # Hanya sertakan objek (tabel) yang ada di metadata target Anda.
    # Ini akan mengabaikan tabel lain di database yang tidak ada di Base.metadata Anda.
    if type_ == "table":
        print(target_metadata.tables)
        return name in target_metadata.tables

    return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
