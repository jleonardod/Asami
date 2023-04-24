def cliente_final_schema(info_pedido) -> dict:
    return {"nombre" : info_pedido["NombreClienteEntrega"],
            "identificacion" : info_pedido["ClienteEntrega"],
            "telefono" : info_pedido["TelefonoEntrega"],
            "direccion" : info_pedido["DireccionEntrega"],
            "ciudad": int(info_pedido["CountyId"])}