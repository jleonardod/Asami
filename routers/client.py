from fastapi import APIRouter, status, Depends
from db.conexion import DAO
from db.schemas.client import client_schema
from db.models.client import Client


router = APIRouter()

# Path - Requerido
@router.get("/{id}")
async def user(id: str):
    return search_user("id", id)

def search_user(field: str, key):
    dao = DAO()
    try:
        client = dao.search_client(field, key)
        print(client)
        return Client(**client_schema(client))
    except:
        return { "error": "No se ha encontrado el usuario!!" }