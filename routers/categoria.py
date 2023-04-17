### API ### 
from fastapi import HTTPException, status

### Database ###
from db.conexion import DAO

### Schemas ###
from db.schemas.categoria import categoria_schema

### Models ###
from db.models.categoria import Categoria

### General ###
from general.numeric import is_numeric

async def list_categorias(id_familia : int | None):
    dao = DAO()
    try:
        categorias = dao.list_categorys(id_familia)
        return categorias
    except:
        return {"error" : "No se pudo acceder a los colores"}

async def buscar_categoria(x_subcategoria : str | None):

    if x_subcategoria:
        is_number = is_numeric(x_subcategoria)
        
        if is_number:
            field = 'id'
        else: 
            field = 'nombre'
        
        categoria = await search_category(field, x_subcategoria)
        
        if categoria is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La sub-categoria no existe")
        else:
            return categoria.id
        
    else:
        return None
    
async def search_category(field, x_subcategoria):
    dao = DAO()
    try:
        categoria = dao.search_categoria(field, x_subcategoria)
        return Categoria(**categoria_schema(categoria))
    except:
        return None
