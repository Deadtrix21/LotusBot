from PythonSrc.Utilities.Imports.System import *
from PythonSrc.Utilities.Imports.Discord import *
from PythonSrc.Utilities import Logger

from .features.Player import MusicPlayerInterface

Log = Logger.GetLogger(__name__)


class MaficMusic(Cog):
    GUILD_VC_TIMER = {}

    def __init__(self, bot):
        self.bot = bot
        self.Players: dict[MusicPlayerInterface] = {}

    async def GetPlayer(self, ctx):
        if ctx.guild.id in self.Players.keys():
            return self.Players[ctx.guild.id]
        else:
            _ = MusicPlayerInterface(self.bot, ctx)
            self.Players[ctx.guild.id] = _
            return _

    async def DelPlayer(self, id):
        if id in self.Players.keys():
            del self.Players[id]
            return

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # if event is triggered by the bot? return
        if member.id == self.bot.user.id:
            return

        # when before.channel != None that means user has left a channel
        if before.channel != None:
            voice = discord.utils.get(self.bot.voice_clients, channel__guild__id=before.channel.guild.id)

            # voice is voiceClient and if it's none? that means the bot is not in an y VC of the Guild that triggerd this event
            if voice == None:
                return

            # if VC left by the user is not equal to the VC that bot is in? then return
            if voice.channel.id != before.channel.id:
                return

            # if VC has only 1 member (including the bot)
            if len(voice.channel.members) <= 1:

                self.GUILD_VC_TIMER[before.channel.guild.id] = 0

                while True:
                    await asyncio.sleep(1)
                    self.GUILD_VC_TIMER[before.channel.guild.id] += 1
                    # if vc has more than 1 member or bot is already disconnectd ? break
                    if len(voice.channel.members) >= 2 or not voice.is_connected():
                        break
                    # if bot has been alone in the VC for more than 60 seconds ? disconnect
                    if self.GUILD_VC_TIMER[before.channel.guild.id] >= 15:
                        await self.DelPlayer(before.channel.guild.id)
                        await voice.disconnect()
                        return

    @commands.command()
    async def play(self, ctx: Context, *, query: str):
        """Play a song.

        query:
            The song to search or play.
        """
        player: MusicPlayerInterface = await self.GetPlayer(ctx)
        if not ctx.guild.voice_client:
            await player.wait_voice_connection()
        await player.play(query)


def setup(bot):
    c = MaficMusic(bot)
    bot.add_cog(c)
