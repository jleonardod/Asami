### Database ###
from db.conexion import DAO

### API ###
from fastapi import HTTPException, status

### Models ###
from db.models.familia import Familia

### Schemas ###
from db.schemas.familia import familia_schema

### General ###
from general.numeric import is_numeric

async def list_families(flags : dict | None, atributos : dict | None):
    dao = DAO()
    try:
        familias = dao.list_familias(flags, atributos)
        return familias
    except:
        return {"error" : "No se pudo acceder a los colores"}


async def buscar_familia(x_familia : str | None):

    if x_familia:
        is_number = is_numeric(x_familia)
        
        if is_number:
            field = 'id'
        else: 
            field = 'nombre'
        
        familia = await search_familia(field, x_familia)
        
        if familia is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La categoria no existe")
        else:
            return familia.id
        
    else:
        return None
    
async def search_familia(field : str, x_familia : str | None):
    dao = DAO()
    try:
        familia = dao.search_familia(field, x_familia)
        return Familia(**familia_schema(familia))
    except:
        return None

