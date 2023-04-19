### API ###
from fastapi import HTTPException, status

### Database ###
from db.conexion import DAO

### Schemas ###
from db.schemas.mark import marks_schema, mark_schema_json

### Models ###
from db.models.mark import Mark

### General ###
from general.numeric import is_numeric

async def list_marks(flags : dict | None, atributos : dict):
    dao = DAO()
    try:
        marks = dao.list_mark(flags, atributos)
        return marks_schema(marks)
    except:
        return {"error" : "No se pudo acceder a las marcas"}
    
async def buscar_marca(x_marks : str | None):
    if x_marks:
        is_number = is_numeric(x_marks)
        
        if is_number:
            field = 'id'
        else: 
            field = 'nombre'
        
        marca = await search_mark(field, x_marks)
        
        if marca is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La marca no existe")
        else:
            return marca.id
        
    else:
        return None
    
async def search_mark(field, x_mark):
    dao = DAO()
    try:
        marca = dao.search_mark(field, x_mark)
        return Mark(**mark_schema_json(marca))
    except:
        return None