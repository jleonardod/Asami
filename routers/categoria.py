### Database ###
from db.conexion import DAO

### Schemas ###
from db.schemas.categoria import categoria_schema

### Models ###
from db.models.categoria import Categoria

async def list_categorias():
    dao = DAO()
    try:
        categorias = dao.list_categorys()
        return categorias
    except:
        return {"error" : "No se pudo acceder a los colores"}
    
async def search_categoria(x_categoria):
    dao = DAO()
    try:
        categoria = dao.search_categoria(x_categoria)
        return Categoria(**categoria_schema(categoria))
    except:
        return None