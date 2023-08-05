from utils.orm_imp import *


class Economy(BaseModel):
    bank: Optional[int] = 0
    wallet: Optional[int] = 0


class User(Document):
    dn_id: int
    email: str
    password: str
    economy: Optional[Economy]


class Permission(BaseModel):
    name: str


class Role(Document):
    name: str
    permission: Optional[List[Permission]] = None


class Account(Document):
    dn_id: int
    role:Link[Role]