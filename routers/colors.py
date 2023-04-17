### Database ###
from db.conexion import DAO

### Schemas ###
from db.schemas.color import colors_catalogo_schema

### Models ###


async def list_colors(familia : int | None):
    dao = DAO()
    try:
        colors = dao.list_colors( familia )
        return colors_catalogo_schema(colors)
    except:
        return {"error" : "No se pudo acceder a los colores"}