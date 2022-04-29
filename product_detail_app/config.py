from dotenv import find_dotenv
from starlette.config import Config
from sqlalchemy.engine.url import URL


config = Config(find_dotenv())
DEBUG = config("DEBUG", cast=bool, default=False)
DATABASE_HOST = config("DATABASE_HOST", default=None)
DATABASE_USER = config("DATABASE_USER", default=None)
DATABASE_NAME = config("DATABASE_NAME", default=None)
DATABASE_PASSWORD = config("DATABASE_PASSWORD", default=None)
DATABASE_PORT = config("DATABASE_PORT", cast=int, default=5432)
DATABASE_URL = config("DATABASE_URL", default=None)
MIN_DB_CONN = config("MIN_DB_CONN", default=5) 
MAX_DB_CONN = config("MAX_DB_CONN", default=10)

DATABASE_URL = URL(
    "postgresql",
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_NAME,
    {"binary_parameters": "yes"},
)