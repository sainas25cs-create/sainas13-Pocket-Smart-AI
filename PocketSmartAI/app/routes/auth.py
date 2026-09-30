from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db
from app.models.entities import User
from app.security import (
    create_access_token,
    hash_password,
    verify_password,
)


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "error": None,
        },
    )


@router.post("/register")
def register_user(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    name = name.strip()
    email = email.strip().lower()

    if len(name) < 2:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "error": "Name must contain at least 2 characters.",
                "name": name,
                "email": email,
            },
            status_code=400,
        )

    if len(password) < 6:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "error": "Password must contain at least 6 characters.",
                "name": name,
                "email": email,
            },
            status_code=400,
        )

    existing_user = db.scalar(
        select(User).where(User.email == email)
    )

    if existing_user:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "error": "An account with this email already exists.",
                "name": name,
                "email": email,
            },
            status_code=400,
        )

    user = User(
        name=name,
        email=email,
        password_hash=hash_password(password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return RedirectResponse(
        url="/login?registered=1",
        status_code=303,
    )


@router.get("/login", response_class=HTMLResponse)
def login_page(
    request: Request,
    registered: int = 0,
):
    message = None

    if registered:
        message = "Registration successful. Please log in."

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "error": None,
            "message": message,
        },
    )


@router.post("/login")
def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    email = email.strip().lower()

    user = db.scalar(
        select(User).where(User.email == email)
    )

    if user is None or not verify_password(
        password,
        user.password_hash,
    ):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "error": "Invalid email or password.",
                "message": None,
                "email": email,
            },
            status_code=401,
        )

    token = create_access_token(user.id)

    response = RedirectResponse(
        url="/dashboard",
        status_code=303,
    )

    response.set_cookie(
        key=settings.COOKIE_NAME,
        value=token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=False,
    )

    return response


@router.post("/logout")
def logout_user():
    response = RedirectResponse(
        url="/",
        status_code=303,
    )

    response.delete_cookie(
        key=settings.COOKIE_NAME,
    )

    return response