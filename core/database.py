from utils.CommonImports import *
from utils.OrmImports import *
from models import repo as Entity


class DataBaseLayer:
    def __init__(self):
        self.local_prod()
        self.__db = self.__client["DiscordDatabase"]
        self.token_config = None

    def local_prod(self):
        if os.getenv('APP_ENV') == "prod":
            self.__client = AsyncIOMotorClient(
                f"mongodb+srv://{os.getenv('USER')}:{os.getenv('PSW')}@{os.getenv('CLUSTER')}/?retryWrites=true&w=majority")
        else:
            self.__client = AsyncIOMotorClient(f"mongodb://localhost:27017/")

    async def __pre__init__orm__(self):
        await init_beanie(database=self.__db, document_models=[
            Entity.Token, Entity.Work, Entity.User,
            Entity.Occupation
        ])

    async def __current__token__(self, name: str):
        self.token_config = await Entity.Token.find_one(Entity.Token.name == name)

    async def PreHookDatabase(self, name: str) -> Entity.Token:
        await self.__pre__init__orm__()
        await self.__current__token__(name)
