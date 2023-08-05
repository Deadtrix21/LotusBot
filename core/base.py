import os

import discord
from utils.master_imp import *
from utils.orm_models import *
from .database import DataBaseLayer


class NightMareAutoSharded(AutoShardedBot):
    def __init__(self):
        super().__init__("x", intents=discord.Intents.default().all(), case_insensitive=True)
        self.__database_layer__ = DataBaseLayer()

    async def on_connect(self):
        self.load_extension(f"extentions.Admin")
        self.load_extension(f"extentions.Account")
        self.load_extension(f"extentions.Economy")
        self.load_extension(f"extentions.Status")
        return await super().on_connect()

    async def on_ready(self):
        app = await self.application_info()
        print(f"App Name: {app.name}")
        print(f"App by {app.owner.name}")

    def connect_database(self):
        self.loop.run_until_complete(self.__database_layer__.PreHookDatabase(os.getenv("NAME")))

    def BootProcess(self):
        self.connect_database()
        self.run(self.__database_layer__.token_config.token)
