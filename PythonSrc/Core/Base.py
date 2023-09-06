from PythonSrc.Utilities.Misc.Database import rEnv
from mafic import NodePool
from PythonSrc.Utilities.Imports import System, Database, Discord
from PythonSrc.Utilities import Logger
from PythonSrc.Utilities.Misc import Database
from PythonSrc.Core.Configurations import Configure
from PythonSrc.Core.Database import DatabaseLayer

Log = Logger.SetLogger(__name__)


with open('.env.yml', 'r') as file:
    primary_service = System.yaml.safe_load(file)['discord']

class NightmareLotus(Discord.AutoShardedBot):
    def __init__(self):
        super().__init__(primary_service['app-configs']["prefix"], intents=Discord.Intents.default().all(), case_insensitive=True)
        self.primary_service = primary_service[primary_service["app-env"]]
        self.configure = Configure()
        self.__database_layer__ = DatabaseLayer(self.loop, self.primary_service)
        self.pool = NodePool(self)


    @Log.catch()
    async def setup_mafic(self):
        try:
            await self.pool.create_node(
                host=self.primary_service["lavalink"]["host"],
                port=self.primary_service["lavalink"]["port"],
                label="MAIN",
                password=self.primary_service["lavalink"]["password"],
            )
            Log.trace(f"Loaded - [ Mafic Voice Connection ]")
        except Exception as e:
            Log.critical(f"Unavailable - [ Mafic Voice Connection ] : {e}")

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
        extension_c = primary_service["app-configs"]["ext"]
        for file in System.os.listdir(System.os.getcwd() + extension_c["directory"]):
            extensions.append(file)
        for ext in extensions:
            extension = extension_c["load-directory"] + ext
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
        self.run(self.__database_layer__.get_token_config(self.primary_service["access-name"]).token)
