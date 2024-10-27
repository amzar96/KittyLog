import logging
from core import models
from fastapi import FastAPI
from config import cfg as CFG
from function import users, cats
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from core.db import engine
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth, OAuthError

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI(
    title="KittyLog",
    description="API for KittyLog",
    version="0.0.1",
    docs_url="/docs",
)

app.add_middleware(SessionMiddleware, secret_key="THISisSECRETkey!!^$^**")
# app.mount("/static", StaticFiles(directory="static"))

oauth = OAuth()
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=CFG.CLIENT_ID,
    client_secret=CFG.CLIENT_SECRET,
    client_kwargs={
        "scope": "email openid profile",
        "redirect_url": CFG.CLIENT_REDIRECT_URL,
    },
)

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


@app.get("/health")
async def root():
    return {"message": "server is up"}


@app.get("/")
def login(request: Request):
    user = request.session.get("user")

    if user:
        return RedirectResponse("home")

    return templates.TemplateResponse("main.html", {"request": request})


@app.get("/home")
async def home(request: Request):
    user = request.session.get("user")

    if not user:
        RedirectResponse("/")
    return templates.TemplateResponse("home.html", {"request": request, "user": user})


@app.get("/login")
async def login(request: Request):
    url = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, url)


@app.get("/auth")
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        logger.error(e)
        return templates.TemplateResponse("error.html", {"request": request})

    user = token.get("userinfo")

    if user:
        request.session["user"] = dict(user)

        if not users.get_user_by_email(user.email):
            logger.info("User not exist in db")
            user = users.create_user(user)
            logger.info(f"User {user} is now created in db")

    return RedirectResponse("home")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
