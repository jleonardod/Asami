def color_schema(color) -> dict:
    return {"id": int(color[0]),
            "nombre": color[1]}

def color_catalogo_schema(color) -> str:
    return color[1]

def colors_catalogo_schema(colors) -> list:
    return [color_catalogo_schema(color) for color in colors]