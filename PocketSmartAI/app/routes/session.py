from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get(
    "/",
    response_class=HTMLResponse,
)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        },
    )


@router.get(
    "/login",
    response_class=HTMLResponse,
)
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request
        },
    )


@router.get(
    "/register",
    response_class=HTMLResponse,
)
def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {
            "request": request
        },
    )


@router.get(
    "/dashboard",
    response_class=HTMLResponse,
)
def dashboard_page(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request
        },
    )


@router.get(
    "/history",
    response_class=HTMLResponse,
)
def history_page(request: Request):
    return templates.TemplateResponse(
        "history.html",
        {
            "request": request
        },
    )


@router.get(
    "/logout",
)
def logout(request: Request):
    response = RedirectResponse(
        url="/login",
        status_code=303,
    )

    response.delete_cookie("access_token")
    response.delete_cookie("token")
    response.delete_cookie("session")

    return response


@router.get(
    "/planner/{kind}",
    response_class=HTMLResponse,
)
def planner_page(
    request: Request,
    kind: str,
):
    allowed = {
        "home",
        "party",
        "jewelry",
    }

    if kind not in allowed:
        kind = "home"

    return templates.TemplateResponse(
        f"{kind}.html",
        {
            "request": request
        },
    )