from PythonSrc.Utilities.Imports.System import *
from PythonSrc.Utilities.Imports.Discord import *
from PythonSrc.Utilities import Logger
from mafic import NodePool, Player, Playlist, Track, TrackEndEvent, SearchType
from .Queue import PlayerQueue


class MusicPlayerInterface:
    def __init__(self, bot: AutoShardedBot, ctx: Context) -> None:
        self.bot: AutoShardedBot = bot
        self.ctx: Context = ctx
        self.voice_connection: discord.VoiceClient | None = None

        self.mp: MusicPlayer | None = None

    async def wait_voice_join(self):
        if not self.ctx.author.voice or not self.ctx.author.voice.channel:
            return await self.ctx.send("You are not in a voice channel.")
        channel = self.ctx.author.voice.channel
        connected = await channel.connect(cls=Player)
        await self.ctx.send(f"Joined {channel.mention}.")
        return connected

    async def wait_voice_connection(self):
        guild_connection = None
        while True:
            if not self.voice_connection:
                self.voice_connection = await self.wait_voice_join()
                guild_connection = self.ctx.guild.voice_client.channel
            else:
                break
        self.mp = MusicPlayer(self.bot, guild_connection, self.voice_connection, self.ctx)

    async def play(self, query: str):
        await self.mp.search_tracks(query)


class MusicPlayer(Player):
    def __init__(self, bot: AutoShardedBot, GuildChannel, voice_connection, ctx: Context) -> None:
        super().__init__(bot, GuildChannel)
        self.bot: AutoShardedBot = bot
        self.ctx: Context = ctx
        self.voice_connection: discord.VoiceClient = voice_connection

    async def search_tracks(self, query: str, search_engine: SearchType = SearchType.SOUNDCLOUD):
        tracks = await self.fetch_tracks(query, search_engine)
        if not tracks:
            return await self.ctx.send("No tracks found.")
        track: Track = tracks[0]
        await self.voice_connection.play(track)

# class MusicPlayer(Player):
#     def __init__(self, client: AutoShardedBot, ctx) -> None:
#         super().__init__(client, ctx.author.voice.channel)
#         self.__queue: PlayerQueue = PlayerQueue()
#         self.__voice_client = None
#         self.ctx: commands.Context = ctx
#         self.bot = client
#
#     async def __auto_connect(self):
#         if not self.ctx.voice_client:
#             self.__voice_client = await self.ctx.author.voice.channel.connect(cls=Player)
#             self.channel = self.__voice_client
#         else:
#             self.__voice_client = self.ctx.voice_client
#             self.channel = self.__voice_client
#
#     async def __wait_voice_connection(self):
#         while True:
#             await self.__auto_connect()
#             if self.__voice_client:
#                 break
#         return
#
#     async def search_tracks(self, query: str, search_engine: SearchType = SearchType.SOUNDCLOUD):
#         await self.__wait_voice_connection()
#         tracks = await self.fetch_tracks(query, search_engine)
#         if not tracks:
#             return await self.ctx.send("No tracks found.")
#         track: Track = tracks[0]
#         await self.__queue.set_next_track(track)
#         await self.__voice_client.play(track)
#
#     async def leave_voice_channel(self):
#         if self.__voice_client:
#             await self.__voice_client.stop()
#             await self.ctx.voice_client.disconnect()
