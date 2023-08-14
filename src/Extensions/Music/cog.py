from ...Utilities.Imports.SysImports import *
from ...Utilities.Imports.DiscordImports import *
import wavelink
from wavelink.ext import spotify
from .features import utils


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def SoundCloud(self, ctx: commands.Context, *, search: str) -> None:
        """Simple play command."""

        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        tracks: list[wavelink.SoundCloudTrack] = await wavelink.SoundCloudTrack.search(search)
        if not tracks:
            await ctx.send(f'Sorry I could not find any songs with search: `{search}`')
            return

        track: wavelink.SoundCloudTrack = tracks[0]
        await vc.play(track)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def Youtube(self, ctx: commands.Context, *, search: str) -> None:
        """Simple play command."""

        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        tracks: list[wavelink.YouTubeTrack] = await wavelink.YouTubeTrack.search(search)
        if not tracks:
            await ctx.send(f'Sorry I could not find any songs with search: `{search}`')
            return

        track: wavelink.YouTubeTrack = tracks[0]
        await vc.play(track)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def Spotify(self, ctx: commands.Context, *, search: str) -> None:
        """Simple play command that accepts a Spotify song URL.

        This command enables AutoPlay. AutoPlay finds songs automatically when used with Spotify.
        Tracks added to the Queue will be played in front (Before) of those added by AutoPlay.
        """

        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        # Check the search to see if it matches a valid Spotify URL...
        decoded = spotify.decode_url(search)
        if not decoded or decoded['type'] is not spotify.SpotifySearchType.track:
            await ctx.send('Only Spotify Track URLs are valid.')
            return

        # Set autoplay to True. This can be disabled at anytime...
        vc.autoplay = True

        tracks: list[spotify.SpotifyTrack] = await spotify.SpotifyTrack.search(search)
        if not tracks:
            await ctx.send('This does not appear to be a valid Spotify URL.')
            return

        track: spotify.SpotifyTrack = tracks[0]

        # IF the player is not playing immediately play the song...
        # otherwise put it in the queue...
        if not vc.is_playing():
            await vc.play(track, populate=True)
        else:
            await vc.queue.put_wait(track)

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
        vc: wavelink.Player = ctx.voice_client
        await vc.stop()


def setup(bot):
    cog = (Music(bot))
    bot.add_cog(cog)
