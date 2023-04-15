from fastapi import APIRouter, Header, Depends, status, HTTPException
from dependencies import get_token_header

### Database ###
from db.conexion import DAO

### Schemas ###
from db.schemas.product import products_schema
from db.schemas.catalogo import catalogo_schema

### Metodos ###
from .categoria import list_categorias, search_categoria
from .marks import list_marks

router = APIRouter(prefix="/product",
                   tags=["products/"],
                   dependencies=[Depends(get_token_header)],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

@router.get("/")
async def products(x_categoria : str | None = Header(default=None),
                   x_subcategoria : str | None = Header(default=None),
                   x_marks : str | None = Header(default=None),
                   x_disponibilidad : str | None = Header(default=None),
                   x_partnum : str | None = Header(default=None),
                   x_descuento : str | None = Header(default=None),
                   x_precioinicial : str | None = Header(default=None),
                   x_preciofinal : str | None = Header(default=None),
                   x_palabraclave : str | None = Header(default=None),
                   x_productonuevo : str | None = Header(default=None),
                   x_color : str | None = Header(default=None)):
    
    if x_categoria:
        is_number = await is_numeric(x_categoria)
        
        if not is_number:
            categoria = await search_categoria(x_categoria)
            if categoria is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La categoria no existe")
            else:
                id_categoria = categoria.id
        else:
            id_categoria = x_categoria

    try:
        prods = await list_products(id_categoria)
        marks = await list_marks(id_categoria)
        colores = await list_colors()
        categorys = await list_categorias()
        productos = catalogo_schema(prods, marks, len(prods), colores, categorys)
        return productos
    except:
        return {"mensaje" : "Ha ocurrido un error"}
    
async def is_numeric(flag : str):
    try:
        complex(flag)
        return True
    except:
        return False

async def list_products(categoria : int | None):
    
    dao = DAO()
    try:
        products = dao.list_products(categoria)
        return products_schema(products)
    except:
        return {"error" : "No se pudo acceder a los productos"}
    
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
    

