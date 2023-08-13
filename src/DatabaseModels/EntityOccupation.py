from ..Utilities.Imports.DatabaseImports import *
from .EntityWork import Work


class Occupation(Document):
    level: int = 0
    exp: int = 0
    last_work_day: str = ""
    work: Optional[Link[Work]] = None
