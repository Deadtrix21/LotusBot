from src.utils.database_models import *
from .Occupation import Occupation
from .Economy import Economy


class User(Document):
    dn_id: str
    email: str
    password: str
    disabled: bool = False
    economy: Optional[Economy] = None
    occupation: Optional[Link[Occupation]] = None
