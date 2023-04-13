from fastapi import APIRouter
from db.conexion import DAO
from db.models.product import Product
from db.schemas.product import products_schema

router = APIRouter()

@router.get("/")
async def products():
    dao = DAO()
    try:
        products = dao.list_products()
        return products_schema(products)
    except:
        return {"error" : "No se pudo acceder a los productos"}

async def list_product():
    dao = DAO()
    try:
        products = dao.list_products()
        print(products)
        return products
    except:
        return {"error" : "No se pudo acceder a los productos"}
