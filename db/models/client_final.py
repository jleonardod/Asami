from pydantic import BaseModel

class ClientFinal(BaseModel):
    nombre : str
    identificacion : str
    telefono : str
    direccion : str
    ciudad : int