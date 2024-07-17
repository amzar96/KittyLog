import os
import configparser
from config import cfg as CFG


def home_dir():
    return os.getcwd()


def get_database_url():
    return f"postgresql+psycopg2://{CFG.DB_USER}:{CFG.DB_PASSWORD}@{CFG.DB_HOST}:{CFG.DB_PORT}/{CFG.DB_NAME}"


config_file_path = f"{home_dir()}/db/alembic.ini"


def update_alembic_config():
    config = configparser.ConfigParser()
    config.read(config_file_path)

    config["alembic"]["sqlalchemy.url"] = get_database_url()

    with open(config_file_path, "w") as configfile:
        config.write(configfile)
