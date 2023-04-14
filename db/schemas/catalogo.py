def catalogo_schema(products, marks, cantidad_productos, colores, categorias) -> dict:
    return {"paginado" : 
            {"CantidadProductos" : cantidad_productos, 
             "Marcas" : marks,
             "Colores" : colores,
             "Categorias" : categorias},
            "ListaProductos" : products}