from fastapi import APIRouter, Header, Depends, status, HTTPException
from dependencies import get_token_header

### Database ###
from db.conexion import DAO

### Schemas ###
from db.schemas.product import products_schema
from db.schemas.catalogo import catalogo_schema

### Metodos ###
from routers.categoria import list_categorias, buscar_categoria
from routers.marks import list_marks
from routers.colors import list_colors
from routers.familia import list_families, buscar_familia

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
    
    id_familia = await buscar_familia(x_categoria)
    id_categoria = await buscar_categoria(x_subcategoria)

    flags = {"familia" : id_familia, "subcategoria" : id_categoria}
    items_busqueda = {}

    for nombre, valor in flags.items():
        if not valor is None:
            items_busqueda[nombre] = valor
    
    try:
        prods = await list_products(items_busqueda)
        marks = await list_marks(id_familia)
        colores = await list_colors(id_familia)
        familias = await list_families(id_familia)
        categorys = await list_categorias(id_familia)
        productos = catalogo_schema(prods, marks, len(prods), colores, categorys, familias)

        if(len(prods) > 0):
            return productos
        else:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existen productos")
    except:
        return {"mensaje" : "Ha ocurrido un error"}

async def list_products(flags : dict):
    
    dao = DAO()
    try:
        products = dao.list_products(flags)
        return products_schema(products)
    except:
        return {"error" : "No se pudo acceder a los productos"}


    

