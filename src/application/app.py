from data.db_manager import DbManager


class App:
    def __init__(self, dbm: DbManager):
        self.dbm = dbm