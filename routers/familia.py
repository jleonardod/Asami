### Database ###
from db.conexion import DAO

### API ###
from fastapi import HTTPException, status

### Models ###
from db.models.familia import Familia

### Schemas ###
from db.schemas.familia import familia_schema

async def list_families(id_familia : int | None):
    dao = DAO()
    try:
        familias = dao.list_familias(id_familia)
        return familias
    except:
        return {"error" : "No se pudo acceder a los colores"}


async def buscar_familia(x_familia : str | None):

    if x_familia:
        is_number = await is_numeric(x_familia)
        
        if not is_number:
            familia = await search_familia(x_familia)
            if familia is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La categoria no existe")
            else:
                return familia.id
        else:
            return x_familia
    else:
        return None
    
async def search_familia(x_familia : str | None):
    dao = DAO()
    try:
        familia = dao.search_familia(x_familia)
        return Familia(**familia_schema(familia))
    except:
        return None

async def is_numeric(flag : str):
    try:
        complex(flag)
        return True
    except:
        return False