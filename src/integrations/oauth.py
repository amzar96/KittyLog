from authlib.integrations.starlette_client import OAuth

from src.config import settings

oauth = OAuth()
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    client_kwargs={
        "scope": "email openid profile",
        "redirect_url": settings.GOOGLE_REDIRECT_URL,
    },
)
