import wavelink
from wavelink.ext import spotify
from ....Utilities.Imports.DiscordImports import *
from ....Utilities.Imports.SysImports import *


class CustomPlayer:
    def __init__(self, bot, ctx):
        self.bot: AutoShardedBot = bot
        self.ctx: commands.Context = ctx

        self.next = asyncio.Event()
        self.queue = asyncio.Queue()
        self.set_equal = 'Flat'
        self.player_volume = 10
        self.now_playing = None

        self.wavelink_player: wavelink.Player = None
        self.bot.loop.create_task(self.player_config())
        self.bot.loop.create_task(self.player_config())

    async def ConnectChannel(self):
        if not self.ctx.voice_client:
            self.wavelink_player = await self.ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            self.wavelink_player = self.ctx.voice_client

    def get_stream(self, link: str):
        if (not link.startswith("https://") and not link.startswith("http://")):
            return link
        if link.startswith("https://"):
            stripped = link.strip("https://")
        if link.startswith("http://"):
            stripped = link.strip("http://")
        if stripped.startswith("www"):
            stripped = stripped.strip("www.")
        stripped = stripped.split(".")
        return stripped[0]

    async def search(self, name: str):
        tracks = None
        stream_type = self.get_stream(name)
        if (stream_type == "open"):
            decoded = spotify.decode_url(name)
            if not decoded or decoded['type'] is not spotify.SpotifySearchType.track:
                await self.ctx.send('Only Spotify Track URLs are valid.')
                return
            tracks: list[spotify.SpotifyTrack] = await spotify.SpotifyTrack.search(name)
        else:
            if self.ctx.author.id == 1030567019617202296:
                tracks: list[wavelink.YouTubeTrack] = await wavelink.YouTubeTrack.search(name)

        if not tracks:
            return await self.ctx.send('No song available.')
        if not self.wavelink_player.is_playing():
            await self.send_nowplaying_embed(tracks[0])
            await self.wavelink_player.play(tracks[0], populate=True)
        else:
            await self.send_add_embed(tracks[0])
            await self.wavelink_player.queue.put_wait(tracks[0])

    async def send_nowplaying_embed(self, song):
        em = Embed(
            color=0x000c30,
            title=f"Now Playing - {song}"
        )
        await self.ctx.send(embed=em)

    async def send_add_embed(self, song):
        em = Embed(
            color=0x000c30,
            title=f"Add {song}"
        )
        await self.ctx.send(embed=em)

    async def player_config(self):
        await self.bot.wait_until_ready()
        await self.ConnectChannel()
        self.wavelink_player.autoplay = False
        await self.wavelink_player.set_volume(self.player_volume)

    async def disconnect_from(self):
        if (len(self.ctx.voice_client.client.users) == 0):
            return True

    async def get_player(self):
        return self.wavelink_player

    async def skip(self):
        await self.wavelink_player.stop()
        await self.wavelink_player.play(await self.wavelink_player.queue.get_wait(), populate=True)
