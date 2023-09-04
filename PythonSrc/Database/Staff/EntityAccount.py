from PythonSrc.Utilities.Imports.Database import *
from .EntityRole import Role


class Account(Document):
    dn_id: str
    role: Link[Role]
