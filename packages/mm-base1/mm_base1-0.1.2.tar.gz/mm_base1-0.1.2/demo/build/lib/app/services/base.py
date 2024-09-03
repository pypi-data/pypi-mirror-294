from dataclasses import dataclass

from mm_base1.services.base import BaseService, BaseServiceParams

from app.db import DB


@dataclass
class AppServiceParams:
    base_params: BaseServiceParams
    db: DB


class AppService(BaseService):
    def __init__(self, app_service_params: AppServiceParams):
        super().__init__(app_service_params.base_params)
        self.db = app_service_params.db
