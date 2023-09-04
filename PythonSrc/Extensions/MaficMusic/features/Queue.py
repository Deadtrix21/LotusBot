from PythonSrc.Utilities.Imports.System import *
from PythonSrc.Utilities.Imports.Discord import *
from PythonSrc.Utilities import Logger
from PythonSrc.Static.mafic import NodePool, Player, Playlist, Track, TrackEndEvent, SearchType




class PlayerQueue:
    def __init__(self):
        self.__queue: asyncio.Queue[Track] = asyncio.Queue()

    async def fetch_next_track(self) -> Track:
        return await self.__queue.get()

    async def set_next_track(self, _data: Track) -> None:
        return await self.__queue.put(_data)

    async def get_queue_size(self) -> int:
        return self.__queue.qsize()


