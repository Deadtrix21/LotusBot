import os

from ..Utilities.Imports.SysLogger import SetLogger
from ..Utilities.Imports.DiscordImports import *
from ..Utilities.Imports.SysImports import *
from ..Utilities.Misc.DatabaseUtilis import read_json
from .database import DatabaseLayer
from mafic import NodePool
import wavelink
from wavelink.ext import spotify

Log = SetLogger(__name__)
JConfig = read_json("base.json")


class NightMareAutoSharded(AutoShardedBot):
    def __init__(self):
        super().__init__("x", intents=discord.Intents.default().all(), case_insensitive=True)
        self.__database_layer__ = DatabaseLayer(self.loop)
        self.pool = NodePool(self)
        # self.loop.create_task(self.add_nodes())

    @Log.catch()
    async def on_connect(self):
        self.load_extension("jishaku")
        self.recursive_load()
        await self.setup_hook()
        await self.setup_mafic()
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

    @Log.catch()
    async def setup_hook(self) -> None:
        pass

    # try:
    #     # Wavelink 2.0 has made connecting Nodes easier... Simply create each Node
    #     # and pass it to NodePool.connect with the client/bot.
    #     sc = spotify.SpotifyClient(
    #         client_id=os.getenv("SPOTIFY"),
    #         client_secret=os.getenv("SPOTIFY_SEC")
    #     )
    #     node: wavelink.Node = wavelink.Node(
    #         uri=f'http://{os.getenv("LAVALINK_HOST")}:{os.getenv("LAVALINK_PORT")}',
    #         password=os.getenv("LAVALINK_PSW"),
    #         retries=10
    #     )
    #     await wavelink.NodePool.connect(client=self, nodes=[node], spotify=sc)
    #     Log.trace(f"Loaded - [ Voice Modules ]")
    # except Exception:
    #     Log.trace(f"Unavailable - [ Voice Modules ]")

    @Log.catch()
    async def setup_mafic(self):
        try:
            await self.pool.create_node(
                host=f"{os.getenv('LAVALINK_HOST')}",
                port=os.getenv("LAVALINK_PORT"),
                label="MAIN",
                password=os.getenv("LAVALINK_PSW"),
            )
            Log.trace(f"Loaded - [ Mafic Voice Connection ]")
        except Exception:
            Log.trace(f"Unavailable - [ Mafic Voice Connection ]")

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
