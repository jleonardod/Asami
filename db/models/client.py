from pydantic import BaseModel

class Client(BaseModel):
    id: int | None
    create_time: str | None
    name: str
    last_name: str
    identification: str
    username: str
    email: str
    phone: str
    city: int
    country: int
    location: str
    type: int
    status: int