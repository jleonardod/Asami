from pydantic import BaseModel

class ClientLog(BaseModel):
    username: str
    profile: int
    password: str
    status: int
    id: int