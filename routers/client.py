from fastapi import APIRouter, status
from db.conexion import DAO
from db.schemas.client import client_schema
from db.models.client import Client

router = APIRouter(prefix="/client",
                  tags=["client"],
                  responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

# Path - Requerido
@router.get("/{id}")
async def user(id: str):
    return search_user("id", id)

def search_user(field: str, key):
    dao = DAO()
    try:
        client = dao.search_client(field, key)
        return Client(**client_schema(client))
    except:
        return { "error": "No se ha encontrado el usuario!!" }