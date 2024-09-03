from mm_base1.db import BaseDB, DatabaseAny
from mm_mongo import MongoCollection

from app.models import Data


class DB(BaseDB):
    def __init__(self, database: DatabaseAny):
        super().__init__(database)
        self.data: MongoCollection[Data] = Data.init_collection(database)
