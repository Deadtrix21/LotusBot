from utils.OrmImports import *
from .EntityOccupation import Occupation
from .EntityEconomy import Economy


class User(Document):
    dn_id: str
    email: str
    password: str
    disabled: bool = False
    economy: Optional[Economy] = None
    occupation: Optional[Link[Occupation]] = None
