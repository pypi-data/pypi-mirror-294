from app.config import AppConfig, DConfigSettings, DValueSettings
from app.db import DB
from app.services.base import AppServiceParams
from app.services.main_service import DataService
from mm_base1.app import BaseApp


class App(BaseApp):
    def __init__(self) -> None:
        super().__init__(AppConfig(), DConfigSettings(), DValueSettings())
        self.db = DB(self.database)
        # services
        self.data_service = DataService(self.base_params)
        # scheduler
        self.scheduler.add_job(self.data_service.generate_data, 6000)

        self.startup()

    @property
    def base_params(self) -> AppServiceParams:  # type: ignore[override]
        return AppServiceParams(super().base_params, self.db)
