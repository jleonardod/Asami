import mysql.connector
from mysql.connector import Error

class DAO():
    def __init__(self):
        try:
            self.conexion = mysql.connector.connect(
                host = 'localhost',
                port = 3306,
                user = 'root',
                password = 'Periferia',
                database = 'asami'
            )
        except Error as ex:
            print("Error al intentar la conexión: {0}".format(ex))

    def search_client(self, field, key):
        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                sql = "SELECT * FROM client WHERE {0} = '{1}'"
                cursor.execute(sql.format(field, key))
                client = cursor.fetchone()
                return client
            except Error as ex:
                print("Error al intentar la conexión: {0}".format(ex))

    def search_full_log(self, field, key):
        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                sql = "SELECT l.username, l.profile, l.password, l.status, c.id FROM client_log l INNER JOIN client c ON l.client = c.id WHERE l.{0} = '{1}'"
                cursor.execute(sql.format(field, key))
                client = cursor.fetchone()
                return client
            except Error as ex:
                print("Error al intentar la conexión: {0}".format(ex))

    def list_products(self, flags : dict | None, atributos : dict | None):

        if len(flags) > 0 or len(atributos) > 0:
            condition = ajustar_condition(flags, atributos)
        else:
            condition = ""

        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                sql = "SELECT p.*, f.{0}, c.{0}, m.{0}, d.{0}, t.{0}, l.{0} FROM product p {1} familia f ON p.familia = f.id {1} categoria c ON p.categoria = c.id {1} marks m ON p.marks = m.id {1} currency_def d ON p.currencyDef = d.id {1} tributari_classification t ON p.tributariClassification = t.id {1} color l ON p.color = l.id {2}"
                cursor.execute(sql.format("nombre", "INNER JOIN", condition))
                # print(sql.format("nombre", "INNER JOIN", condition))
                products = cursor.fetchall()
                return products
            except Error as ex:
                print("Error al intentar la conexión: {0}".format(ex))

    def list_mark(self, flags : dict | None, atributos : dict | None):
        
        sql = "SELECT DISTINCT m.* FROM marks m"
        if len(flags) > 0 or len(atributos) > 0:
            sql += " INNER JOIN product p ON m.id = p.marks "
            condition = ajustar_condition(flags, atributos)
            sql += condition
        
        #print(atributos)
        #print(sql)

        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                
                cursor.execute(sql)
                products = cursor.fetchall()
                return products
            except Error as ex:
                print("Error al intentar la conexión: {0}".format(ex))

    def list_colors(self, flags : dict | None, atributos : dict | None):
        sql = "SELECT DISTINCT c.* FROM color c"
        if len(flags) > 0 or len(atributos) > 0:
            sql += " INNER JOIN product p ON c.id = p.color "
            condition = ajustar_condition(flags, atributos)
            sql += condition

        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                
                cursor.execute(sql)
                products = cursor.fetchall()
                return products
            except Error as ex:
                print("Error al intentar la conexión: {0}".format(ex))

    def search_mark(self, field, x_mark):
        
        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                sql = "SELECT * FROM marks WHERE {0} = '{1}'"
                cursor.execute(sql.format(field, x_mark))
                marca = cursor.fetchone()
                return marca
            except Error as ex:
                print("Error al intentar la conexión: {0}".format(ex))

    def list_categorys(self, flags : dict | None, atributos : dict | None):
        sql = "SELECT DISTINCT c.* FROM categoria c"
        if len(flags) > 0 or len(atributos) > 0:
            sql += " INNER JOIN product p ON c.id = p.categoria "
            condition = ajustar_condition(flags, atributos)
            sql += condition

        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                cursor.execute(sql)
                products = cursor.fetchall()
                return products
            except Error as ex:
                print("Error al intentar la conexión: {0}".format(ex))

    def list_familias(self, flags : dict | None, atributos : dict | None):
        sql = "SELECT DISTINCT f.* FROM familia f"
        if len(flags) > 0 or len(atributos) > 0:
            sql += " INNER JOIN product p ON f.id = p.familia "
            condition = ajustar_condition(flags, atributos)
            sql += condition
        
        # print(sql)

        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                cursor.execute(sql)
                products = cursor.fetchall()
                return products
            except Error as ex:
                print("Error al intentar la conexión: {0}".format(ex))

    def search_categoria(self, field, x_categoria):
        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                sql = "SELECT * FROM categoria WHERE {0} = '{1}'"
                cursor.execute(sql.format(field, x_categoria))
                products = cursor.fetchone()
                return products
            except Error as ex:
                print("Error al intentar la conexión: {0}".format(ex))

    def search_familia(self, field : str | None, familia : str | None):
        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                sql = "SELECT * FROM familia WHERE {0} = '{1}'"
                cursor.execute(sql.format(field, familia))
                products = cursor.fetchone()
                return products
            except Error as ex:
                print("Error al intentar la conexión: {0}".format(ex))

    def crear_cliente_final(self, cliente_final, id_cliente : int):
        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                sql = "INSERT INTO final_client(nombre, identificacion, telefono, direccion, ciudad, id_client) VALUES ('{0}', '{1}', '{2}', '{3}', {4}, {5})"
                cursor.execute(sql.format(cliente_final.nombre, cliente_final.identificacion, cliente_final.telefono, cliente_final.direccion, cliente_final.ciudad, id_cliente))
                self.conexion.commit()
                return cursor.lastrowid
            except Error as ex:
                print("Error al intentar conexión: {0}".format(ex))

    def buscar_producto(self, field : str | None, key : str | None):
        condition = "WHERE {0} = '{1}'"
        condition = condition.format(field, key)
        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                sql = "SELECT p.*, f.{0}, c.{0}, m.{0}, d.{0}, t.{0}, l.{0} FROM product p {1} familia f ON p.familia = f.id {1} categoria c ON p.categoria = c.id {1} marks m ON p.marks = m.id {1} currency_def d ON p.currencyDef = d.id {1} tributari_classification t ON p.tributariClassification = t.id {1} color l ON p.color = l.id {2}"
                cursor.execute(sql.format("nombre", "INNER JOIN", condition))
                # print(sql.format("nombre", "INNER JOIN", condition))
                product = cursor.fetchone()
                return product
            except Error as ex:
                print("Error al intentar la conexión: {0}".format(ex))

    def insertar_pedido(self, id_cliente : int, id_final_client : int, products : list, fecha_hora : str):
        cadena_productos = ','.join([str(item) for item in products])
        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                sql = "INSERT INTO pedido(cliente, cliente_final, products, fecha_hora) VALUES ({0}, {1}, '{2}', '{3}')"
                cursor.execute(sql.format(id_cliente, id_final_client, cadena_productos, fecha_hora))
                self.conexion.commit()
                return cursor.lastrowid
            except Error as ex:
                print("Error al intentar conexión: {0}".format(ex))

    def update_producto(self, field: str, id : int, new_value):
        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                sql = "UPDATE product SET {0} = '{1}' WHERE id = {2}"
                cursor.execute(sql.format(field, new_value, id))
                self.conexion.commit()
                return cursor.lastrowid
            except Error as ex:
                print("Error al intentar conexión: {0}".format(ex))

def ajustar_condition(flags : dict, atributos : dict):
    contador = 0
    condition = ""
    condition_complete = ""
    use_where = False
    # print(atributos)

    for nombre, valor in flags.items():
        if nombre == "subcategoria":
            nombre = "categoria"

        if contador == 0:
            condition += " WHERE "
            use_where = True
        else: 
            condition += " AND "
                
        condition += "{0} = {1}"
        condition = condition.format(nombre, valor)
                
        contador = contador+1

    condition_complete = condition

    for nombre, valor in atributos.items():

        if not valor is None:
            if use_where:
                condition_complete += " AND "
            else:
                condition_complete += " WHERE "
                use_where = True

            if nombre == "quantity":
                if valor == "1":
                    valor = "> 0"
                else:
                    valor = "< 1"
            elif nombre == "color":
                nombre = "l.nombre"
                valor = "= '"+ valor + "'"
            elif nombre == "precio_inicial":
                nombre = "precio"
                valor = "> "+ valor
            elif nombre == "precio_final":
                nombre = "precio"
                valor = "< "+ valor
            elif nombre == "palabra_clave":
                nombre = "name"
                valor = "LIKE '%" + valor + "%'"
            else :
                valor = "= '"+ valor + "'"
        
            # atributos["quantity"] = valor
            condition_complete += "{0} {1}"
            condition_complete = condition_complete.format(nombre, valor)

    # print(condition_complete)

    condition = condition_complete
    

    return condition
            