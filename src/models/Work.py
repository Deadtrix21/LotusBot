from src.utils.database_models import *



class Work(Document):
    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    level: int
    name: str
    daily_rate: int = 0
    daily_exp: int = 0

