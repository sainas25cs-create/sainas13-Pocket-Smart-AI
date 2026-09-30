from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.entities import User
from app.security import get_current_user


router = APIRouter()


# ---------------------------------------------------------
# Template directory
# ---------------------------------------------------------
# pages.py location:
# app/routes/pages.py
#
# parent.parent => app/
# so templates path becomes:
# app/templates/
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)


# =========================================================
# HOME PAGE
# =========================================================

@router.get("/", response_class=HTMLResponse)
def home_page(
    request: Request,
    db: Session = Depends(get_db),
):
    user = None

    try:
        from app.security import get_user_from_token

        user = get_user_from_token(request, db)

    except Exception:
        user = None

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "user": user,
        },
    )


# =========================================================
# DASHBOARD
# =========================================================

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(
    request: Request,
    user: User = Depends(get_current_user),
):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "user": user,
        },
    )


# =========================================================
# INTERIOR
# =========================================================

@router.get("/interior", response_class=HTMLResponse)
def interior_page(
    request: Request,
    user: User = Depends(get_current_user),
):
    return templates.TemplateResponse(
        request=request,
        name="interior.html",
        context={
            "user": user,
        },
    )


# =========================================================
# PARTY
# =========================================================

@router.get("/party", response_class=HTMLResponse)
def party_page(
    request: Request,
    user: User = Depends(get_current_user),
):
    return templates.TemplateResponse(
        request=request,
        name="party.html",
        context={
            "user": user,
        },
    )


# =========================================================
# JEWELRY
# =========================================================

@router.get("/jewelry", response_class=HTMLResponse)
def jewelry_page(
    request: Request,
    user: User = Depends(get_current_user),
):
    return templates.TemplateResponse(
        request=request,
        name="jewelry.html",
        context={
            "user": user,
        },
    )


# =========================================================
# HISTORY
# =========================================================

@router.get("/history", response_class=HTMLResponse)
def history_page(
    request: Request,
    user: User = Depends(get_current_user),
):
    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "user": user,
        },
    )