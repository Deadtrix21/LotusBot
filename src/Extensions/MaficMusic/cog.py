from ...Utilities.Imports.SysLogger import GetLogger
from ...Exceptions.CustomExceptions import *

from humanfriendly import format_timespan, parse_timespan


from .features.Player import MusicPlayer

Log = GetLogger(__name__)


class MaficMusic(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Players = {}

    async def GetPlayer(self, ctx):
        if ctx.guild.id in self.Players.keys():
            return self.Players[ctx.guild.id]
        else:
            _ = MusicPlayer(self.bot, ctx)
            self.Players[ctx.guild.id] = _
            return _

    async def DelPlayer(self, id):
        if id in self.Players.keys():
            del self.Players[id]
            return

    @commands.command()
    async def play(self, ctx: commands.Context, *, query: str):
        """Play a song.

        query:
            The song to search or play.
        """
        player: MusicPlayer = await self.GetPlayer(ctx)
        await player.search_tracks(query)




def setup(bot):
    c = MaficMusic(bot)
    bot.add_cog(c)
