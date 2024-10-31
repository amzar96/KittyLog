import logging
from core import models, schemas
from core.db import engine
from typing import Annotated
from datetime import datetime
from config import cfg as CFG
from function import users, cats
from starlette.requests import Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi import FastAPI, Form, status, HTTPException
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
def main(request: Request):
    user = request.session.get("user")

    if user:
        return RedirectResponse("home")

    return templates.TemplateResponse(
        "main.html", {"request": request, "user_login": {"is_user": user}}
    )


@app.get("/home")
async def home(request: Request):
    user = request.session.get("user").copy()
    error_message = request.session.pop("error_message", None)
    if not user:
        RedirectResponse("/")

    cats_list = cats.get_cats_by_owner_email(user.get("email"))

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "user": user,
            "user_login": {"is_user": user},
            "error_message": error_message,
            "cats": cats_list,
        },
    )


@app.get("/login")
async def login(request: Request):
    url = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, url)


@app.get("/logout")
async def logout(request: Request):
    request.session.pop("user")
    return RedirectResponse("/")


@app.get("/auth")
async def auth(request: Request):
    try:
        logger.info(request)
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        logger.error(e)
        return templates.TemplateResponse(
            "error.html", {"request": request, "user_login": {"is_user": user}}
        )

    user = token.get("userinfo")

    logger.info(user)

    if user:
        request.session["user"] = user

        if not users.get_user_by_email(user.email):
            logger.info("User not exist in db")
            user = users.create_user(user)
            logger.info(f"User {user} is now created in db")

    return RedirectResponse("home")


@app.post("/cat", response_model=schemas.CatBase)
async def add_cat(
    request: Request,
    cat: schemas.CatCreate,
):
    user = request.session.get("user").copy()

    try:
        user = users.get_user_by_email(user.get("email"))

        cat = cats.create_cat(cat.name, cat.nickname, cat.dob, user)
        logger.info(f"Cat {cat.name} is now created in db")

        return cat

    except Exception as e:
        logger.error(e)
        if "already registered" in str(e):
            request.session["error_message"] = "Cat already registered!"

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cat already registered!",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error while adding cat!",
            )


@app.put("/cat", response_model=schemas.ResponseModel)
async def edit_cat(
    request: Request,
    payload: schemas.CatUpdate,
):
    user = request.session.get("user").copy()

    user = users.get_user_by_email(user.get("email"))
    query = cats.update_cat(payload, user)

    if query:
        return {
            "data": None,
            "message": f"Cat ({payload.name}) is updated in db",
        }
    else:
        error_msg = "Error on updating.. try again"
        request.session["error_message"] = error_msg
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg,
        )


@app.delete("/cat/{cat_id}", response_model=schemas.ResponseModel)
async def delete_cat(request: Request, cat_id: str):
    cat = cats.get_cat_by_id(value=cat_id)
    query = cats.delete_cat(cat)

    if query:
        return {
            "data": None,
            "message": f"Cat ({cat_id}) is deleted in db",
        }
    else:
        error_msg = "Error on deleting.. try again"
        request.session["error_message"] = error_msg
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg,
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
