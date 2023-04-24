from db.conexion import DAO

from db.models.client_final import ClientFinal


async def crear_final_client(client : ClientFinal, id_cliente):
    dao = DAO()
    try:
        cliente_final = dao.crear_cliente_final(client, id_cliente)
        return cliente_final
    except:
        return {"mensaje" : "Error al consultar"}