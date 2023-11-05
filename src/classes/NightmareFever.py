# // Imports
from src.utils.base_imports import *

# // Services
from src.services.DatabaseService import DatabaseService
from src.services.ExtensionService import ExtensionService
from src.services.MusicService import MusicService
from src.services.PrimaryService import PrimaryService
from src.services.LogService import SpecificLog

Logger = SpecificLog(__name__)

# // Helpers
from src.utils.helpers import discord_intents


class NightmareLotus(AutoShardedBot):
    primary_service: PrimaryService
    database_service: DatabaseService

    music_service: MusicService
    extension_service: ExtensionService

    def __init__(self):
        self.primary_service = PrimaryService()
        self.start_time = arrow.utcnow()
        super().__init__(
            when_mentioned_or(*self.primary_service.get_config()["app-configs"]["prefix"]),
            intents=discord_intents(),
            case_insensitive=True
        )

    async def on_ready(self) -> None:
        app = await self.application_info()
        Logger.success(f"App Name - {app.name} | Made by - {app.owner.name} | {len(self.shards)}")
        await self.start_services()

    def hook_services(self) -> None:
        self.database_service = DatabaseService(self.loop, self.primary_service.get_env_config())
        self.music_service = MusicService(self, self.primary_service.get_env_config())
        self.extension_service = ExtensionService(self)

    async def start_services(self) -> None:
        await self.wait_until_ready()
        await self.music_service.connect_nodes()
        await self.extension_service.start_loader()

    async def close(self) -> None:
        self.database_service.close()
        await super().close()

    def run(self):
        self.hook_services()
        super().run(self.database_service.get_token().token)
