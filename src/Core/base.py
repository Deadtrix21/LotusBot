import os

from ..Utilities.Imports.SysLogger import SetLogger
from ..Utilities.Imports.DiscordImports import *
from ..Utilities.Imports.SysImports import *
from ..Utilities.Misc.DatabaseUtilis import read_json
from .database import DatabaseLayer
import mafic

Log = SetLogger(__name__)
JConfig = read_json("base.json")


class NightMareAutoSharded(AutoShardedBot):
    def __init__(self):
        super().__init__("x", intents=discord.Intents.default().all(), case_insensitive=True)
        self.__database_layer__ = DatabaseLayer(self.loop)
        self.pool = mafic.NodePool(self)
        self.loop.create_task(self.add_nodes())

    @Log.catch()
    async def on_connect(self):
        self.load_extension("jishaku")
        self.recursive_load()
        return await super().on_connect()

    @Log.catch()
    def recursive_load(self):
        extensions = []
        for file in os.listdir(os.getcwd() + JConfig["ext_dir"]):
            extensions.append(file)
        for ext in extensions:
            self.LoadExtension(ext)

    def LoadExtension(self, name: str) -> list[str]:
        try:
            self.load_extension(JConfig["load_ext"] + name)
            Log.trace(f"Loaded - [ {name} ]")
        except BaseException as E:
            Log.critical(E)

    async def add_nodes(self):
        Log.trace(f"Loaded - [ Voice Modules ]")
        await self.pool.create_node(
            host=os.getenv("LAVALINK_HOST"),
            port=os.getenv("LAVALINK_PORT"),
            label="MAIN",
            password=os.getenv("LAVALINK_PSW"),
        )

    @Log.catch()
    async def on_ready(self):
        app = await self.application_info()
        print(f"App Name: {app.name}")
        print(f"App by {app.owner.name}")

    @Log.catch()
    def connect_database(self):
        self.__database_layer__.connect_database()
        self.__database_layer__.connect_orm()

    @Log.catch()
    def BootProcess(self):
        self.connect_database()
        self.run(self.__database_layer__.get_token_config(os.getenv("NAME")).token)
