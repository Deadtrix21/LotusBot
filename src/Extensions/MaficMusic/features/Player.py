from mafic import NodePool, Player, Playlist, Track, TrackEndEvent, SearchType
from ....Utilities.Imports.SysLogger import GetLogger
from ....Utilities.Imports.SysImports import *
from ....Utilities.Imports.DiscordImports import *
from .Queue import PlayerQueue


class MusicPlayer(Player):
    def __init__(self, client: AutoShardedBot, ctx) -> None:
        super().__init__(client, ctx.author.voice.channel)
        self.__queue: PlayerQueue = PlayerQueue()
        self.__voice_client = None
        self.ctx: commands.Context = ctx
        self.bot = client

    async def __auto_connect(self):
        if not self.ctx.voice_client:
            self.__voice_client = await self.ctx.author.voice.channel.connect(cls=Player)
        else:
            self.__voice_client = self.ctx.voice_client

    async def __wait_voice_connection(self):
        while True:
            await self.__auto_connect()
            if self.__voice_client:
                break
        return

    async def search_tracks(self, query: str, search_engine: SearchType = SearchType.SOUNDCLOUD):
        await self.__wait_voice_connection()
        tracks = await self.fetch_tracks(query, search_engine)
        if not tracks:
            return await self.ctx.send("No tracks found.")
        track: Track = tracks[0]
        await self.__queue.set_next_track(track)
        await self.__voice_client.play(track)
