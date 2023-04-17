### Database ###
from db.conexion import DAO

### Schemas ###
from db.schemas.categoria import categoria_schema

### Models ###
from db.models.categoria import Categoria

async def list_categorias(id_familia : int | None):
    dao = DAO()
    try:
        categorias = dao.list_categorys(id_familia)
        return categorias
    except:
        return {"error" : "No se pudo acceder a los colores"}