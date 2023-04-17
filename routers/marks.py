### Database ###
from db.conexion import DAO

### Schemas ###
from db.schemas.mark import marks_schema

### Models ###
from db.models.mark import Mark

async def list_marks(flags : dict | None):
    dao = DAO()
    try:
        marks = dao.list_mark(flags)
        return marks_schema(marks)
    except:
        return {"error" : "No se pudo acceder a las marcas"}