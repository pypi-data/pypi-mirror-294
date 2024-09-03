from mm_base1.server import AppRouter

from app.app import App
from app.routers import api_router, ui_router


def init_routers(app: App, templates):
    return [
        AppRouter(api_router.init(app), prefix="/api", tag="main"),
        AppRouter(ui_router.init(app, templates), tag="ui"),
    ]
