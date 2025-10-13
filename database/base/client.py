# pylint: disable=C0114
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_HOST = os.getenv("PI5_POSTGRES_DB_HOST", "localhost")
DATABASE_USER = os.getenv("PI5_POSTGRES_DB_USER", "postgres")
DATABASE_PWD = os.getenv("PI5_POSTGRES_DB_PWD", "password")
DATABASE_PORT = os.getenv("PI5_POSTGRES_DB_PORT", "5432")
DATABASE_NAME = os.getenv("PI5_POSTGRES_DB_NAME", "postgres")
DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PWD}@\
{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

engine = create_engine(
    DATABASE_URL
)

DBSession = sessionmaker(autoflush=False, autocommit=False, bind=engine) # pylint: disable=C0103
