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

    def list_products(self):
        if self.conexion.is_connected():
            try:
                cursor = self.conexion.cursor()
                sql = "SELECT * FROM product"
                cursor.execute(sql)
                products = cursor.fetchall()
                return products
            except Error as ex:
                print("Error al intentar la conexión: {0}".format(ex))
            