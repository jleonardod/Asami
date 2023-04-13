from pydantic import BaseModel

class Client(BaseModel):
    id: int | None
    name: str
    last_name: str
    identification: str
    email: str
    phone: str
    city: int
    country: int
    location: str
    type: int