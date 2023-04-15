from pydantic import BaseModel

class Mark(BaseModel):
    id : int | None
    nombre : str | None