from mm_mongo import MongoCollection

from app.models import Data
from mm_base1.db import DatabaseAny


class DB:
    def __init__(self, database: DatabaseAny):
        self.data: MongoCollection[Data] = Data.init_collection(database)
