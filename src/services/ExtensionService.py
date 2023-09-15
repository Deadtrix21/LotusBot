from src.utils.base_imports import os, typing

from src.services.LogService import SpecificLog
Logger = SpecificLog(__name__)

if typing.TYPE_CHECKING:
    from src.classes.NightmareFever import NightmareLotus


class ExtensionService:
    def __init__(self, bot):
        self.bot: NightmareLotus = bot
        self.extension_path: str = self.bot.primary_service.get_config()["app-configs"]["ext-directory"]
        self.listener_path: str = self.bot.primary_service.get_config()["app-configs"]["listeners-directory"]

    async def load_extensions(self):
        extensions = []
        for listenfile in os.listdir(os.getcwd() + "/" + self.listener_path):
            extensions.append(f"{self.listener_path.replace('/', '.')}{listenfile}")
        for extfile in os.listdir(os.getcwd() + "/" + self.extension_path):
            extensions.append(f"{self.extension_path.replace('/', '.')}{extfile}")
        for ext in extensions:
            module_name = ext.split('.')[-1]
            try:
                self.bot.load_extension(ext)
                Logger.success(f"Loaded {module_name}")
            except Exception as e:
                Logger.critical(e)





