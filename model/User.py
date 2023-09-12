from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str
    password: str
    role: Optional[list] = []

    def asJSON(self):
        return self.model_dump()