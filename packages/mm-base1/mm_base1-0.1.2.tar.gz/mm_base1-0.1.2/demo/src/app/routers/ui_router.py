from fastapi import APIRouter
from mm_base1.jinja import Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app.app import App


def init(app: App, templates: Templates) -> APIRouter:
    router = APIRouter()

    @router.get("/", response_class=HTMLResponse)
    def index_page(req: Request):
        return templates.render(req, "index.j2")

    @router.get("/data", response_class=HTMLResponse)
    def data_page(req: Request):
        data = app.db.data.find({}, "-created_at", 100)
        return templates.render(req, "data.j2", {"data": data})

    return router
