import typing

from src.utils.base_imports import *
from mafic import Player, Playlist, Track, TrackEndEvent, SearchType, NoNodesAvailable

if typing.TYPE_CHECKING:
    from src.classes.NightmareFever import NightmareLotus


class MusicPlayer(Player):
    def __init__(self, bot, channel) -> None:
        super().__init__(bot, channel)
        self.bot: NightmareLotus = bot
        self.ctx: typing.Union[commands.Context, None] = None
        self.now_playing = None

    async def set_ctx(self, ctx):
        self.ctx = ctx

    async def next_song(self):
        print("trying to play next song")

    async def pause_song(self):
        currentSong: typing.Union[None, Track] = super().current
        await self.ctx.send(f"Paused {currentSong.title}")

    async def resume_song(self):
        currentSong: typing.Union[None, Track] = super().current
        await self.ctx.send(f"Resume playing {currentSong.title}")

    async def search_tracks(self, query: str, search_engine: SearchType = SearchType.SOUNDCLOUD):
        tracks = await self.fetch_tracks(query, search_engine)
        if not tracks:
            return await self.ctx.send("No tracks found.")
        track: Track = tracks[0]
        await self.play(track)

    async def skip_track(self):
        await self.stop()

    async def pause_track(self):
        await self.pause_song()
        await super().pause()

    async def resume_track(self):
        await self.resume_song()
        await super().resume()
