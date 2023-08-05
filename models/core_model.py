from utils.orm_imp import *

class Token(Document):
    name: str
    token: str