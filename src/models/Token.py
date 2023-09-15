from src.utils.database_models import *


class Token(Document):
    name: str
    token: str
