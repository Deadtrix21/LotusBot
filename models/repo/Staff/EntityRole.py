from utils.OrmImports import *
from .EntityPermission import Permission


class Role(Document):
    name: str
    permission: Optional[List[Permission]] = None
