from fastapi import APIRouter
from mm_mongo import mongo_query

from app.app import App
from app.models import DataStatus


def init(app: App) -> APIRouter:
    router = APIRouter()

    @router.get("")
    def get_data_list(worker: str | None = None, status: DataStatus | None = None, limit: int = 100):
        return app.db.data.find(mongo_query(worker=worker, status=status), "-created_at", limit)

    @router.post("/generate")
    def generate_data():
        return app.main_service.generate_data()

    @router.get("/{pk}")
    def get_data(pk):
        return app.db.data.get_or_none(pk)

    @router.delete("/{pk}")
    def delete_data(pk):
        return app.db.data.delete_by_id(pk)

    return router
