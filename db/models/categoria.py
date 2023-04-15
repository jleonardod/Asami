from pydantic import BaseModel

class Categoria(BaseModel):
    id: int | None
    nombre: str | None