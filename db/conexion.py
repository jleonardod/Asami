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
                sql = "SELECT * FROM client WHERE {0} = {1}"
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

    def list_products(self, categoria : int | None):
        if self.conexion.is_connected():
            condition = "WHERE "
            try:
                cursor = self.conexion.cursor()
                sql = "SELECT p.*, f.{0}, c.{0}, m.{0}, d.{0}, t.{0}, l.{0} FROM product p {1} familia f ON p.familia = f.id {1} categoria c ON p.categoria = c.id {1} marks m ON p.marks = m.id {1} currency_def d ON p.currencyDef = d.id {1} tributari_classification t ON p.tributariClassification = t.id {1} color l ON p.color = l.id {2}"
                
                if categoria:
                    
                    condition += "familia = "
                    condition += str(categoria)
                    
                else:
                    condition = ""
                
                cursor.execute(sql.format("nombre", "INNER JOIN", condition))
                products = cursor.fetchall()
                return products
            except Error as ex:
                print("Error al intentar la conexión: {0}".format(ex))

    def list_mark(self, categoria : int | None):
        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                if categoria :
                    sql = "SELECT DISTINCT m.* FROM marks m INNER JOIN product p ON p.marks = m.id WHERE p.categoria = {0}"
                else :
                    sql = "SELECT * FROM marks"
                cursor.execute(sql.format(categoria))
                products = cursor.fetchall()
                return products
            except Error as ex:
                print("Error al intentar la conexión: {0}".format(ex))

    def list_colors(self):
        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                sql = "SELECT nombre FROM color"
                cursor.execute(sql)
                products = cursor.fetchall()
                return products
            except Error as ex:
                print("Error al intentar la conexión: {0}".format(ex))

    def list_categorys(self):
        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                sql = "SELECT * FROM categoria"
                cursor.execute(sql)
                products = cursor.fetchall()
                return products
            except Error as ex:
                print("Error al intentar la conexión: {0}".format(ex))

    def search_categoria(self, x_categoria):
        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                sql = "SELECT * FROM familia WHERE nombre = '{0}'"
                cursor.execute(sql.format(x_categoria))
                products = cursor.fetchone()
                return products
            except Error as ex:
                print("Error al intentar la conexión: {0}".format(ex))
            