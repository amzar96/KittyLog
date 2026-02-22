from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool, text

from src.config import settings
from src.shared.models.base import Base

# Register all models for autogenerate support
from src.shared.models import user  # noqa: F401
from src.shared.models import rbac  # noqa: F401
from src.shared.models import subscription  # noqa: F401
from src.domains.cats import models as cats_models  # noqa: F401
from src.domains.health import models as health_models  # noqa: F401
from src.domains.nutrition import models as nutrition_models  # noqa: F401
from src.domains.diary import models as diary_models  # noqa: F401
from src.domains.monitoring import models as monitoring_models  # noqa: F401
from src.domains.appointments import models as appointments_models  # noqa: F401
from src.domains.notifications import models as notifications_models  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", settings.SUPABASE_DB_URL.replace("%", "%%"))

target_metadata = Base.metadata

MANAGED_SCHEMAS = {"kittylog"}


def include_name(name, type_, parent_names):
    if type_ == "schema":
        return name in MANAGED_SCHEMAS
    return True


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema="kittylog",
        include_schemas=True,
        include_name=include_name,
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
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS kittylog"))
        connection.commit()

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema="kittylog",
            include_schemas=True,
            include_name=include_name,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
