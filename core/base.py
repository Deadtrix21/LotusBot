from utils.MasterImports import *
from core.database import DataBaseLayer


class NightMareAutoSharded(AutoShardedBot):
    def __init__(self):
        super().__init__("x", intents=discord.Intents.default().all(), case_insensitive=True)
        self.__database_layer__ = DataBaseLayer()

    async def on_connect(self):
        self.recursive_load()
        return await super().on_connect()

    def recursive_load(self):
        self.LoadExtension('jishaku')
        extensions = []
        for file in os.listdir(os.getcwd() + "/" + "extentions"):
            if file.endswith(".py"):
                extensions.append("extentions" + "." + file[:-3])
        for ext in extensions:
            self.LoadExtension(ext)

    def LoadExtension(self, name: str) -> list[str]:
        try:
            print(f"{name} - Loading")
            self.load_extension(name)
        except Exception as exception:
            print(exception)

    async def on_ready(self):
        app = await self.application_info()
        print(f"App Name: {app.name}")
        print(f"App by {app.owner.name}")

    def connect_database(self):
        self.loop.run_until_complete(self.__database_layer__.PreHookDatabase(os.getenv("NAME")))

    def BootProcess(self):
        self.connect_database()
        self.run(self.__database_layer__.token_config.token)
