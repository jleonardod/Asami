### API ###
from fastapi import APIRouter, Header, Depends, status, HTTPException
from dependencies import get_token_header

### Database ###
from db.conexion import DAO

### Schemas ###
from db.schemas.product import products_schema, product_schema
from db.schemas.catalogo import catalogo_schema

### Metodos ###
from routers.categoria import list_categorias, buscar_categoria
from routers.marks import list_marks, buscar_marca
from routers.colors import list_colors
from routers.familia import list_families, buscar_familia

### Models ###
from db.models.product import Product


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
                   x_nuevo : str | None = Header(default=None)):
    
    id_familia = await buscar_familia(x_categoria)
    id_categoria = await buscar_categoria(x_subcategoria)
    id_mark = await buscar_marca(x_marks)

    flags = {"familia" : id_familia, "subcategoria" : id_categoria, "marks" : id_mark}
    items_busqueda = {}
    atributos_producto = {}

    for nombre, valor in flags.items():
        if not valor is None:
            items_busqueda[nombre] = valor

    atributos_producto = await ajustar_atributos(x_disponibilidad, "quantity", atributos_producto)
    atributos_producto = await ajustar_atributos(x_descuento, "descuento", atributos_producto)
    atributos_producto = await ajustar_atributos(x_nuevo, "nuevo", atributos_producto)

    atributos_producto["partNum"] = x_partnum
    atributos_producto["precio_inicial"] = x_precioinicial
    atributos_producto["precio_final"] = x_preciofinal
    atributos_producto["palabra_clave"] = x_palabraclave
    # atributos_producto["color"] = x_color

    # print(atributos_producto)

    try:
        prods = await list_products(items_busqueda, atributos_producto)
        marks = await list_marks(items_busqueda, atributos_producto)
        colores = await list_colors(items_busqueda, atributos_producto)
        familias = await list_families(items_busqueda, atributos_producto)
        categorys = await list_categorias(items_busqueda, atributos_producto)
        productos = catalogo_schema(prods, marks, len(prods), colores, categorys, familias)
    except:
        return {"mensaje" : "Ha ocurrido un error"}
    
    if(len(prods) > 0):
        return productos
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existen productos")

async def list_products(flags : dict, atributos : dict):    
    dao = DAO()
    try:
        products = dao.list_products(flags, atributos)
        return products_schema(products)
    except:
        return {"error" : "No se pudo acceder a los productos"}
    
async def ajustar_atributos(atributo : str | None, nombre : str, atributos_producto : dict):
    
    if atributo == '1' or atributo == '2' or atributo == None:
        atributos_producto[nombre] = atributo
        # print(atributos_producto)
        return atributos_producto
    else:
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Consulta no valida")


async def search_product(field : str, key):
    dao = DAO()
    try:
        producto = dao.buscar_producto(field, key)
        return Product(**product_schema(producto))
    except:
        return None
    
async def actualizar_producto(field : str, cantidad_productos : dict):
    dao = DAO()
    for id, value in cantidad_productos.items():
        new_quantity = value[1] - value[0]
        
        try:
            producto = dao.update_producto(field, id, new_quantity)
        except:
            return False
        
    return True