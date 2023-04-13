from fastapi import APIRouter, status, Depends
from db.conexion import DAO
from db.schemas.client import client_schema
from db.models.client import Client
from db.models.clientLog import ClientLog
from db.schemas.client_log import client_log_schema


router = APIRouter()

# Path - Requerido
@router.get("/{id}")
async def user(id: str):
    return search_client("id", id)

def search_client(field: str, key):
    dao = DAO()
    try:
        client = dao.search_client(field, key)
        return Client(**client_schema(client))
    except:
        return { "error": "No se ha encontrado el usuario!!" }
    
def search_full_log(field: str, key):
    dao = DAO()
    try:
        client = dao.search_full_log(field, key)
        return ClientLog(**client_log_schema(client))
    except:
        return { "error": "No se ha encontrado el usuario!!" }