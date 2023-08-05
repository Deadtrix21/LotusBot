from utils.orm_imp import *


class Economy(BaseModel):
    bank: Optional[float] = 0
    wallet: Optional[float] = 0


class Work(Document):
    level : float
    name : str
    daily_rate : float

class Occupation(Document):
    level : float = 0
    exp : float = 0
    last_work_day : str = ""
    work : Optional[Link[Work]] = None

class User(Document):
    dn_id: str
    email: str
    password: str
    economy: Optional[Economy]
    occupation: Optional[Link[Occupation]] = None


class Permission(BaseModel):
    name: str


class Role(Document):
    name: str
    permission: Optional[List[Permission]] = None


class Account(Document):
    dn_id: str
    role:Link[Role]
