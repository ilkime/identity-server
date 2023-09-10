from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str
    password: str
    role: Optional[list] = []