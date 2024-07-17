from config import common
import schema.models as models
from logging.config import fileConfig


common.update_alembic_config()
fileConfig(common.config_file_path)

target_metadata = models.Base.metadata
