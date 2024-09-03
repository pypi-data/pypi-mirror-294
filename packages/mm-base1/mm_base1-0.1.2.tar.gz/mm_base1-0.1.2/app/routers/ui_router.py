from fastapi import APIRouter
from mm_mongo import mongo_query
from starlette.requests import Request
from starlette.responses import HTMLResponse
from wtforms import Form, IntegerField, SelectField

from app.app import App
from app.models import DataStatus
from mm_base1.jinja import Templates, form_choices


class DataFilterForm(Form):  # type: ignore
    status = SelectField(choices=form_choices(DataStatus, title="status"), default="")
    limit = IntegerField(default=100)


def init(app: App, templates: Templates) -> APIRouter:
    router = APIRouter()

    @router.get("/", response_class=HTMLResponse)
    def index_page(req: Request) -> HTMLResponse:
        return templates.render(req, "index.j2")

    @router.get("/data", response_class=HTMLResponse)
    def data_page(req: Request) -> HTMLResponse:
        form = DataFilterForm(req.query_params)
        query = mongo_query(status=form.data["status"])
        data = app.db.data.find(query, "-created_at", form.data["limit"])
        return templates.render(req, "data.j2", {"form": form, "data": data})

    @router.get("/upload", response_class=HTMLResponse)
    def upload_page(req: Request) -> HTMLResponse:
        return templates.render(req, "upload.j2")

    return router
