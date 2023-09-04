from PythonSrc.Utilities.Imports import System, Database, Discord
from PythonSrc.Utilities import Logger
from PythonSrc.Utilities.Misc import Database
from PythonSrc.Core.Configurations import Configure
from PythonSrc.Core.Database import DatabaseLayer

Log = Logger.SetLogger(__name__)

JConfig = Database.read_json("base.json")


class NightmareLotus(Discord.AutoShardedBot):
    def __init__(self):
        super().__init__("x", intents=Discord.Intents.default().all(), case_insensitive=True)
        self.configure = Configure()
        self.__database_layer__ = DatabaseLayer(self.loop)

    @Log.catch()
    async def setup_mafic(self):
        try:
            await self.pool.create_node(
                host=f"{System.os.getenv('LAVALINK_HOST')}",
                port=System.os.getenv("LAVALINK_PORT"),
                label="MAIN",
                password=System.os.getenv("LAVALINK_PSW"),
            )
            Log.trace(f"Loaded - [ Mafic Voice Connection ]")
        except Exception:
            Log.critical(f"Unavailable - [ Mafic Voice Connection ]")

    @Log.catch()
    async def on_connect(self):
        await self.setup_mafic()
        return await super().on_connect()

    @Log.catch()
    async def on_ready(self):
        app = await self.application_info()
        print("")
        Log.trace(f"App Name - {app.name} | Made by - {app.owner.name}")

    @Log.catch()
    def load_extension(self, name: str) -> list[str]:
        try:
            super().load_extension(name)
            Log.trace(f"Loaded - [ {name.split('.')[-1]} ]")
        except BaseException as E:
            Log.critical(E)

    @Log.catch()
    def recursive_load(self):
        extensions = []
        for file in System.os.listdir(System.os.getcwd() + JConfig["ext_dir"]):
            extensions.append(file)
        for ext in extensions:
            extension = JConfig["load_ext"] + ext
            self.load_extension(extension)

    @Log.catch()
    def connect_database(self):
        self.__database_layer__.connect_database()
        self.__database_layer__.connect_orm()

    @Log.catch()
    def boot(self):
        self.load_extension("jishaku")
        self.recursive_load()
        self.connect_database()
        self.run(self.__database_layer__.get_token_config(System.os.getenv("NAME")).token)
