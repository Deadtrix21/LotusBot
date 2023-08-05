import asyncio

from utils.CommonImports import *


class Status(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.start_up = self.get_startup_time()

    def get_startup_time(self):
        return arrow.utcnow()

    def calc_uptime(self):
        now                     = arrow.get(arrow.utcnow())
        utc                     = arrow.get(self.start_up)
        core                    = now-utc
        seconds                 = core.total_seconds()
        minutes,    seconds     = divmod(seconds, 60)
        hour,       minutes     = divmod(minutes , 60)
        hour                    = round(hour)
        minute                  = round(minutes)
        second                  = round(seconds)
        return f"for {hour} hours, {minute} minutes and {second} seconds"

    def pick_status(self):
        pick = {
            1:Status.calc_uptime(self),
            2:f"to {len(self.bot.guilds)} servers"
        }
        return pick[random.randint(1,2)]

    async def Status__Preview(self):
        while True:
            object_type = discord.ActivityType.streaming
            object_activity = (
                discord.Activity(
                    type=object_type,
                    name=Status.pick_status(self),
                    url="https://www.twitch.tv/DeadTrix0")
            )
            await self.bot.change_presence(status=object_activity, activity=object_activity)
            await asyncio.sleep(5)

def setup(bot):
    n = Status(bot)
    loop = asyncio.get_event_loop()
    loop.create_task(n.Status__Preview())
    bot.add_cog(n)