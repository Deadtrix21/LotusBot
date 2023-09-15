from PythonSrc.Utilities.Imports.Database import *
from .EntityPermission import Permission


class Role(Document):
    name: str
    permission: Optional[List[Permission]] = None
