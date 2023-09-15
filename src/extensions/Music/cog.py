
from discord import VoiceProtocol

from mafic import TrackEndEvent, NoNodesAvailable
from src.utils.base_imports import *
from src.services.LogService import SpecificLog

from .features.MusicPlayer import MusicPlayer

Logger = SpecificLog(__name__)

if typing.TYPE_CHECKING:
    from src.classes.NightmareFever import NightmareLotus


class Music(Extension):

    def __init__(self, bot) -> None:
        self.GUILD_VC_TIMER = None
        self.bot: NightmareLotus = bot

    # @commands.Cog.listener()
    # async def on_track_end(self, event: TrackEndEvent[MusicPlayer]):
    #     player: MusicPlayerInterface = self.PLAYERS[event.player.guild.id]
    #     return await player.player_service.next_song()

    @commands.Cog.listener()
    async def on_track_end(self, event: TrackEndEvent[MusicPlayer]):
        return await event.player.next_song()

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
                        await voice.disconnect()
                        return

    async def cog_before_invoke(self, ctx: commands.Context) -> None:
        should_connect = ctx.command.name in (
            "play",
            "search",
        )
        if not should_connect:
            return False
        player: MusicPlayer | None = ctx.voice_client
        if not player or not player.connected:
            if not ctx.author.voice:
                await ctx.send("I am not connected to a voice channel.")
                return False
            permissions = ctx.author.voice.channel.permissions_for(ctx.me)
            if not permissions.connect or not permissions.speak:
                await ctx.send("I do not have permissions for the channel.")
                return False
            try:
                active_player = await ctx.author.voice.channel.connect(cls=MusicPlayer)
                await active_player.set_ctx(ctx)
                player: MusicPlayer | None = ctx.voice_client
            except NoNodesAvailable:
                await ctx.send("No node available to connect to.")
                return False
            except Exception as e:
                print(e)
                await ctx.send("Failed to connect.")
                return False
            if (player.channel.id != ctx.author.voice.channel.id):
                await ctx.send("You are not in my voice channel.")
                return False
            return True


    @commands.command()
    async def play(self, ctx: commands.Context, *, query: str):
        """Play a song.

        query:
            The song to search or play.
        """
        player: typing.Union[MusicPlayer, VoiceProtocol] = ctx.voice_client
        await player.search_tracks(query)

    @commands.command()
    async def pause(self, ctx: commands.Context):
        """Pause a song.
        """
        player: typing.Union[MusicPlayer, VoiceProtocol] = ctx.voice_client
        await player.pause_track()

    @commands.command()
    async def resume(self, ctx: commands.Context):
        """Pause a song.
        """
        player: typing.Union[MusicPlayer, VoiceProtocol] = ctx.voice_client
        await player.resume_track()

    @commands.command()
    async def stop(self, ctx: commands.Context):
        """Stop playing.
        """
        player: typing.Union[MusicPlayer, VoiceProtocol] = ctx.voice_client
        await player.stop()



def setup(bot):
    n = Music(bot)
    bot.add_cog(n)
