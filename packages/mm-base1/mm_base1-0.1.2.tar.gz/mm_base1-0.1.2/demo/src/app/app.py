from mm_base1.app import BaseApp

from app.config import AppConfig, DConfigSettings, DValueSettings
from app.db import DB
from app.services.base import AppServiceParams
from app.services.main_service import MainService


class App(BaseApp):
    def __init__(self) -> None:
        super().__init__(AppConfig(), DConfigSettings(), DValueSettings())
        self.db: DB = DB(self.database)
        self.main_service = MainService(self.base_params)

        self.scheduler.add_job(self.main_service.generate_data, 600)

        self.startup()

    @property
    def base_params(self) -> AppServiceParams:  # type: ignore[override]
        return AppServiceParams(super().base_params, self.db)
