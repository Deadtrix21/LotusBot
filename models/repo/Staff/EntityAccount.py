from utils.OrmImports import *
from .EntityRole import Role


class Account(Document):
    dn_id: str
    role: Link[Role]
