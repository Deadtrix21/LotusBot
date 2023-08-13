from ..Utilities.Imports.SysImports import *
from .database import DatabaseLayer


class PreDatabase:

    def __init__(self):
        self.__set_asyncio__()
        self.__connect_db()

    def __set_asyncio__(self):
        self.loop = None
        try:
            self.loop = asyncio.get_event_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
        finally:
            self.__database_layer__ = DatabaseLayer(self.loop)

    def __connect_db(self):
        self.__database_layer__.connect_database()
        self.__database_layer__.connect_orm()

    def config_callback(self, func):
        self.loop.run_until_complete(func())