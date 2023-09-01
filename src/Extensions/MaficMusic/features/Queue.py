import asyncio

from mafic import NodePool, Player, Playlist, Track, TrackEndEvent
from src.Utilities.Imports.SysLogger import GetLogger
from src.Utilities.Imports.SysImports import *
from src.Utilities.Imports.DiscordImports import *


class PlayerQueue:
    def __init__(self):
        self.__queue: asyncio.Queue[Track] = asyncio.Queue()

    async def fetch_next_track(self) -> Track:
        return await self.__queue.get()

    async def set_next_track(self, _data: Track) -> None:
        return await self.__queue.put(_data)

    async def get_queue_size(self) -> int:
        return self.__queue.qsize()


