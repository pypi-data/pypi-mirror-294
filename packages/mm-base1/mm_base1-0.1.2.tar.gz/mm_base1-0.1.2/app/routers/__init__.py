from app.app import App
from app.routers import api_router, ui_router
from mm_base1.jinja import Templates
from mm_base1.server import AppRouter


def init_routers(app: App, templates: Templates) -> list[AppRouter]:
    return [
        AppRouter(api_router.init(app), prefix="/api", tag="api"),
        AppRouter(ui_router.init(app, templates), tag="ui"),
    ]
