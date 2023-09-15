from src.utils.database_models import *
from src.models.Token import Token
from src import models

class DatabaseService:
    def __init__(self, loop, config):
        self.db: AsyncIOMotorClient = None
        self.loop = loop
        self.config = config
        self.setup()

    async def __connect_database__(self):
        self.db = AsyncIOMotorClient(self.config["database"]["url"])
        await init_beanie(
            database=self.db["DiscordDatabase"],
            document_models=[
                models.Token,
                models.Work,
                models.User,
                models.Occupation,
            ]
        )

    def get_token(self):
        return self.loop.run_until_complete(Token.find_one(Token.name == self.config["access-name"]))

    def setup(self):
        self.loop.run_until_complete(self.__connect_database__())

    def close(self):
        self.db.close()
