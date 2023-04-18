from fastapi import APIRouter, Header, Depends, status, HTTPException
from dependencies import get_token_header

### Database ###
from db.conexion import DAO

### Schemas ###
from db.schemas.product import products_schema
from db.schemas.catalogo import catalogo_schema

### Metodos ###
from routers.categoria import list_categorias, buscar_categoria
from routers.marks import list_marks, buscar_marca
from routers.colors import list_colors
from routers.familia import list_families, buscar_familia

### General ###
from general.numeric import is_numeric

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
    id_mark = await buscar_marca(x_marks)

    flags = {"familia" : id_familia, "subcategoria" : id_categoria, "marks" : id_mark}
    items_busqueda = {}

    for nombre, valor in flags.items():
        if not valor is None:
            items_busqueda[nombre] = valor
            
    print(x_disponibilidad)
    if x_disponibilidad == '1' or x_disponibilidad == '2':
        items_busqueda["disponibilidad"] = x_disponibilidad
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Disponibilidad no valida")
    
    try:
        prods = await list_products(items_busqueda)
        marks = await list_marks(items_busqueda)
        colores = await list_colors(items_busqueda)
        familias = await list_families(items_busqueda)
        categorys = await list_categorias(items_busqueda)
        productos = catalogo_schema(prods, marks, len(prods), colores, categorys, familias)
    except:
        return {"mensaje" : "Ha ocurrido un error"}
    
    if(len(prods) > 0):
        return productos
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existen productos")

async def list_products(flags : dict):
    
    dao = DAO()
    try:
        products = dao.list_products(flags)
        return products_schema(products)
    except:
        return {"error" : "No se pudo acceder a los productos"}


    

