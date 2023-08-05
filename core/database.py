from utils.CommonImports import *
from utils.orm_imp import *
from utils.orm_models import *


class DataBaseLayer:
    def __init__(self):
        self.__client = AsyncIOMotorClient(f"mongodb+srv://{os.getenv('USER')}:{os.getenv('PSW')}@{os.getenv('CLUSTER')}/?retryWrites=true&w=majority")
        self.__db = self.__client["DiscordDatabase"]
        self.token_config = None

    async def __pre__init__orm__(self):
        await init_beanie(database=self.__db, document_models=[
            Token,
            User,Role,Account
        ])

    async def __current__token__(self, name: str):
        self.token_config = await Token.find_one(Token.name == name)

    async def PreHookDatabase(self, name: str) -> Token:
        await self.__pre__init__orm__()
        await self.__current__token__(name)

