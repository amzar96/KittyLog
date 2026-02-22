import logging

from supabase import Client, create_client

from src.config import settings

logger = logging.getLogger(__name__)


def get_supabase_client() -> Client:
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)


class SupabaseStorage:
    def __init__(self, bucket: str = "cat-photos"):
        self.client = get_supabase_client()
        self.bucket = bucket

    def upload_photo(self, file_bytes: bytes, path: str, content_type: str) -> str:
        self.client.storage.from_(self.bucket).upload(
            path, file_bytes, {"content-type": content_type}
        )
        public_url = self.client.storage.from_(self.bucket).get_public_url(path)
        logger.info("photo uploaded", extra={"path": path})
        return public_url

    def delete_photo(self, path: str) -> None:
        self.client.storage.from_(self.bucket).remove([path])
        logger.info("photo deleted", extra={"path": path})
