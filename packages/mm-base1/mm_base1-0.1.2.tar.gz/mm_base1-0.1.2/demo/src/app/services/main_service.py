import random

from pymongo.results import InsertOneResult

from app.models import Data, DataStatus
from app.services.base import AppService, AppServiceParams


class MainService(AppService):
    def __init__(self, base_params: AppServiceParams) -> None:
        super().__init__(base_params)

    def generate_data(self) -> InsertOneResult:
        status = random.choice(list(DataStatus))
        value = random.randint(0, 1_000_000)
        self.dlog(
            "data_generated",
            {"status": status, "value": value, "large-data": "abc" * 100},
        )
        self.send_telegram_message(f"a new data: {value}")
        return self.db.data.insert_one(Data(status=status, value=value))
