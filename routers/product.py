from fastapi import APIRouter
from db.conexion import DAO
from db.models.product import Product
from db.schemas.product import products_schema
from db.schemas.catalogo import catalogo_schema

router = APIRouter()

@router.get("/")
async def products():
    try:
        prods = await list_products()
        marks = await list_marks()
        colores = await list_colors()
        print(colores)
        categorys = await list_categorias()
        productos = catalogo_schema(prods, marks, len(prods), colores, categorys)
        return productos
    except:
        return {"mensaje" : "Ha ocurrido un error"}

async def list_products():
    dao = DAO()
    try:
        products = dao.list_products()
        return products_schema(products)
    except:
        return {"error" : "No se pudo acceder a los productos"}

async def list_marks():
    dao = DAO()
    try:
        marks = dao.list_mark()
        return marks
    except:
        return {"error" : "No se pudo acceder a las marcas"}
    
async def list_colors():
    dao = DAO()
    try:
        colores = []
        colors = dao.list_colors()
        for color in colors:
            color = str(color)
            color = color.replace(',', '')
            color = color.replace('(', '')
            color = color.replace(')', '')
            color = color.replace("'", "")
            colores.append(color)
        return colores
    except:
        return {"error" : "No se pudo acceder a los colores"}
    
async def list_categorias():
    dao = DAO()
    try:
        categorias = dao.list_categorys()
        return categorias
    except:
        return {"error" : "No se pudo acceder a los colores"}
