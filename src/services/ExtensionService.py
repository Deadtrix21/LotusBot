from src.utils.base_imports import os, typing

from src.services.LogService import SpecificLog

Logger = SpecificLog(__name__)

if typing.TYPE_CHECKING:
    from src.classes.NightmareFever import NightmareLotus


class ExtensionService:
    INITIAL_LOAD: bool = False

    def __init__(self, bot):
        self.bot: NightmareLotus = bot
        self.extension_path: str = self.bot.primary_service.get_config()["app-configs"]["ext-directory"]
        self.listener_path: str = self.bot.primary_service.get_config()["app-configs"]["listeners-directory"]
        self.tasks_path: str = self.bot.primary_service.get_config()["app-configs"]["tasks-directory"]

    @Logger.catch()
    async def start_loader(self):
        if self.INITIAL_LOAD:
            await self.__reload_async()
        if not self.INITIAL_LOAD:
            await self.__load_extensions()
            await self.__load_async()
        self.INITIAL_LOAD = True

    async def __load_extensions(self):
        try:
            self.bot.load_extension("jishaku")
            Logger.success(f"Loaded Jishaku")
        except Exception as e:
            Logger.critical(e)
        extensions = []
        for extfile in os.listdir(os.getcwd() + "/" + self.extension_path):
            extensions.append(f"{self.extension_path.replace('/', '.')}{extfile}")
        for ext in extensions:
            module_name = ext.split('.')[-1]
            try:
                self.bot.load_extension(ext)
                Logger.success(f"Loaded {module_name}")
            except Exception as e:
                Logger.critical(e)

    async def __load_async(self):
        extensions = []
        for listenfile in os.listdir(os.getcwd() + "/" + self.listener_path):
            extensions.append(f"{self.listener_path.replace('/', '.')}{listenfile}")
        for taskfile in os.listdir(os.getcwd() + "/" + self.tasks_path):
            extensions.append(f"{self.tasks_path.replace('/', '.')}{taskfile}")
        for ext in extensions:
            module_name = ext.split('.')[-1]
            try:
                self.bot.load_extension(ext)
                Logger.success(f"Loaded {module_name}")
            except Exception as e:
                Logger.critical(e)

    async def __reload_async(self):
        extensions = []
        for listenfile in os.listdir(os.getcwd() + "/" + self.listener_path):
            extensions.append(f"{self.listener_path.replace('/', '.')}{listenfile}")
        for taskfile in os.listdir(os.getcwd() + "/" + self.tasks_path):
            extensions.append(f"{self.tasks_path.replace('/', '.')}{taskfile}")
        for ext in extensions:
            module_name = ext.split('.')[-1]
            try:
                self.bot.reload_extension(ext)
                Logger.trace(f"Loaded {module_name}")
            except Exception as e:
                Logger.critical(e)
