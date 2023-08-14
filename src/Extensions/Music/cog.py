from ...Utilities.Imports.SysImports import *
from ...Utilities.Imports.DiscordImports import *
import wavelink
from wavelink.ext import spotify
from .features import utils
from .features.BaseClasses import CustomPlayer


class Music(commands.Cog):
    GUILD_VC_TIMER = {}
    def __init__(self, bot):
        self.bot :AutoShardedBot = bot
        self.Players = {}

    async def GetPlayer(self, ctx):
        if ctx.guild.id in self.Players.keys():
            return self.Players[ctx.guild.id]
        else:
            _ = CustomPlayer(self.bot, ctx)
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
            voice = discord.utils.get(self.bot.voice_clients , channel__guild__id = before.channel.guild.id)

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
                    if self.GUILD_VC_TIMER[before.channel.guild.id] >= 30:
                        await self.DelPlayer(before.channel.guild.id)
                        await voice.disconnect()
                        return


    @commands.command()
    async def play(self, ctx: commands.Context, *, query):
        player: CustomPlayer = await self.GetPlayer(ctx)
        await player.search(query)



    @commands.command()
    async def disconnect(self, ctx: commands.Context) -> None:
        """Simple disconnect command.

        This command assumes there is a currently connected Player.
        """
        vc: wavelink.Player = ctx.voice_client
        await vc.disconnect()

    @commands.command()
    async def skip(self, ctx: commands.Context) -> None:
        """Simple skip command.

        This command assumes there is a currently connected Player.
        """
        player: CustomPlayer = await self.GetPlayer(ctx)
        await player.skip()

def setup(bot):
    cog = (Music(bot))
    bot.add_cog(cog)
