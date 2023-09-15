from discord.ext.bridge import AutoShardedBot

import mafic
from src.services.LogService import SpecificLog

Logger = SpecificLog(__name__)


class MusicService:
    def __init__(self, bot: AutoShardedBot, config):
        self.bot = bot
        self.config = config
        self.voice_node = mafic.NodePool(bot)

    async def connect_nodes(self):
        try:
            await self.voice_node.create_node(
                host=self.config["lavalink"]["host"],
                port=self.config["lavalink"]["port"],
                label=(await self.bot.application_info()).name,
                password=self.config["lavalink"]["password"],
                heartbeat=self.config["lavalink"]["heartbeat"],
                secure=self.config["lavalink"]["ssl_enabled"],
            )
            Logger.trace(f"Loaded - [ Mafic Voice Connection ]")
        except Exception as e:
            Logger.critical(f"Unavailable - [ Mafic Voice Connection ] : {e}")


