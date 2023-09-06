from PythonSrc.Core.Database import DatabaseLayer
from PythonSrc.Utilities.Imports.System import *
from PythonSrc.Database import Token, Work, User, Occupation

with open('.env.yml', 'r') as file:
    primary_service = yaml.safe_load(file)['discord']

class PreDatabase:

    def __init__(self):
        self.primary_service = primary_service[primary_service["app-env"]]
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
            self.__database_layer__ = DatabaseLayer(self.loop, self.primary_service)

    def __connect_db(self):
        self.__database_layer__.connect_database()
        self.__database_layer__.connect_orm()

    def config_callback(self, func):
        self.loop.run_until_complete(func())