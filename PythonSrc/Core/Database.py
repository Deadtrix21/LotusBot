from PythonSrc.Utilities.Imports.System import *
from PythonSrc.Utilities.Imports.Database import *
from PythonSrc.Utilities.Misc.Database import rEnv
from PythonSrc.Database import Token, Work, User, Occupation


class DatabaseLayer:
    __client_database__ = None
    __client_connection__ = None

    def __init__(self, bot_loop):
        self.loop = bot_loop
        self.__switch_env__()

    def __switch_env__(self):
        self.connection = None
        if (rEnv("APP_ENV") == "prod"):
            self.connection = f"mongodb+srv://{rEnv('DB_USER')}:{rEnv('DB_PSW')}@{rEnv('DB_CLUSTER')}/?retryWrites=true&w=majority"
        else:
            self.connection = f"mongodb://localhost:27017/"
        return None

    async def __orm_config__(self):
        await init_beanie(
            database=self.__client_database__,
            document_models=[
                Token, Work, User, Occupation
            ]
        )

    async def __get_token__(self, name: str):
        return await Token.find_one(Token.name == name)

    def get_token_config(self, name: str):
        return self.loop.run_until_complete(self.__get_token__(name))

    def connect_database(self):
        self.__client_connection__ = AsyncIOMotorClient(self.connection)
        self.__client_database__ = self.__client_connection__["DiscordDatabase"]

    def connect_orm(self):
        self.loop.run_until_complete(self.__orm_config__())