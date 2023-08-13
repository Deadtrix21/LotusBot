from ...Utilities.Imports.DatabaseImports import *


class Permission(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    name: str
