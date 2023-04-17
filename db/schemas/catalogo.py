def catalogo_schema(products, marks, cantidad_productos, colores, categorias, familias) -> dict:
    return {"paginado" : 
            {"CantidadProductos" : cantidad_productos, 
             "Marcas" : marks,
             "Colores" : colores,
             "Categorias" : familias,
             "SubCategorias" : categorias},
            "ListaProductos" : products}