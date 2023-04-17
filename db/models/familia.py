from pydantic import BaseModel

class Familia(BaseModel):
    id: int | None
    nombre: str | None