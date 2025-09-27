import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/vehicles_db"
)
APP_PORT = int(os.getenv("APP_PORT", 8000))
