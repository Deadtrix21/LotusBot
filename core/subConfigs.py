import asyncio
import os
from utils.MasterImports import *
from .database import DataBaseLayer


class SubConfigurations:
    __database_layer__ = DataBaseLayer()
    def __init__(self):
        self.loop = None
        self.__set_asyncio()
        self.__connect_db()

    def __set_asyncio(self):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        finally:
            self.loop = loop

    def __connect_db(self):
        self.loop.run_until_complete(self.__database_layer__.PreHookDatabase(os.getenv("NAME")))

    def config_callback(self, func):
        self.loop.run_until_complete(func())