from pydantic import BaseModel

class Product(BaseModel):
    id : int | None
    partNum : str
    familia : int
    categoria : int
    name : str
    description : str
    marks : int
    sales_min_price : str
    sales_max_price : str
    precio : str
    currency_def : int
    quantity : str
    tributari_classification : int
    nombre_imagen : str
    descuento : str
    shipping : str
    condition : str
    category : str
    color : int
    width : str
    height : str
    depth : str
    dimensions_unit : str
    weight : str
    weight_unit : str
    shipping_width : str
    shipping_height : str
    shipping_depth : str
    sku : str
    memoria_ram : str
    procesador : str
    disco_duro_gb : str
    disco_duro_tb : str
    disco_duro_ssd_gb : str
    disco_duro_ssd_tb : str