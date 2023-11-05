import arrow
import humanfriendly
from discord import Cog
import random
import discord
import asyncio
from discord.ext import tasks


class Status(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.Status__Preview.start()

    def cog_unload(self):
        self.Status__Preview.cancel()

    def get_startup_time(self):
        return self.bot.start_time

    def calc_uptime(self):
        now = arrow.get(arrow.utcnow())
        utc = self.get_startup_time()
        core = now - utc
        return humanfriendly.format_timespan(core.total_seconds())

    def pick_status(self):
        pick = {
            1: Status.calc_uptime(self),
            2: f"to {len(self.bot.guilds)} servers"
        }
        return pick[random.randint(1, 2)]

    @tasks.loop(seconds=15)
    async def Status__Preview(self):
        object_type = discord.ActivityType.streaming
        object_activity = (
            discord.Activity(
                type=object_type,
                name=Status.pick_status(self),
                url="https://www.twitch.tv/DeadTrix0")
        )
        await self.bot.change_presence(status=object_activity, activity=object_activity)


def setup(bot):
    n = Status(bot)
    bot.add_cog(n)
