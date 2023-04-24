### API ###
from fastapi import APIRouter, Depends, status, Body, HTTPException
from dependencies import get_token_header
from db.conexion import DAO

### Cliente ###
from routers.client import search_client

### Schemas ###
from db.schemas.cliente_final import cliente_final_schema

### Cliente Entrega ###
from routers.cliente_final import crear_final_client

### Model ###
from db.models.client_final import ClientFinal

### Product ###
from routers.product import search_product, actualizar_producto

### General ###
import datetime

router = APIRouter(prefix="/pedido",
                   tags=["pedido/"],
                   dependencies=[Depends(get_token_header)],
                   responses={status.HTTP_404_NOT_FOUND: {"mensaje" : "No encontrado"}})

@router.post("/")
async def pedido(pedido : dict = Body(media_type="application/json")):
    try:
        info_pedido = pedido["listaPedido"][0]
        lista_pedido_detalle = info_pedido["listaPedidoDetalle"]
        products = []
        products_quantity = {}

        for product in lista_pedido_detalle:  
            producto = await search_product("partNum", product["PartNum"])
            
            if not producto is None:
                if product["Cantidad"] <= 0 or product["Cantidad"] > int(producto.quantity):
                    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="La cantidad solicitada del producto no es aceptable")
                else:
                    products.append(producto.id)
                    products_quantity[producto.id] = [product["Cantidad"], int(producto.quantity)]
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El producto no existe")
         
        account_num = info_pedido["AccountNum"]
        cliente = search_client('account_num', account_num)
        if not cliente is None:
            cliente_final = ClientFinal(**cliente_final_schema(info_pedido))
            fecha_hora = str(datetime.datetime.now())
            result_cliente = await crear_final_client(cliente_final, cliente.id)
            #result_cliente = 7
            if not result_cliente is None:
                creacion_pedido = await crear_pedido(cliente.id, result_cliente, products, fecha_hora) 
                #creacion_pedido = 1
                if not creacion_pedido is None:
                    actualizacion_producto = await actualizar_producto('quantity', products_quantity)
                    if actualizacion_producto:
                        return {"mensaje" : "Pedido realizado con exito"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El cliente no fue encontrado")
        # return {"mensaje" : "Pedido realizado con exito"}
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se puede procesar el pedido")
    
async def crear_pedido(id_cliente : int, id_final_client : int, products: list, fecha_hora : str):
    dao = DAO()
    try:
        pedido_creado = dao.insertar_pedido(id_cliente, id_final_client, products, fecha_hora)
        return pedido_creado
    except:
        return None