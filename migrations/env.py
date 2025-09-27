# migrations/env.py
from logging.config import fileConfig
import os
import sys

from alembic import context
from sqlalchemy import engine_from_config, pool

# --- Coloca a RAIZ do projeto no sys.path ---
# estrutura esperada: <repo_root>/migrations/env.py  e <repo_root>/src/...
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# --- Importa o Base do seu projeto ---
from src.adapters.db.base import Base  # garante que Base.metadata exista
import src.adapters.db.models

config = context.config

# --- Log do Alembic ---
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Ponto crítico: define sqlalchemy.url a partir do ambiente ---
db_url = os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))
if not db_url:
    # fallback seguro para desenvolvimento local (ajuste se quiser)
    db_url = "postgresql+psycopg://postgres:postgres@localhost:5432/vehicles_db"
config.set_main_option("sqlalchemy.url", db_url)

# --- Metadata para autogenerate ---
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
