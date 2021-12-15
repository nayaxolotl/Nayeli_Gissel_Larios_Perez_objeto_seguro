import pymysql


class BaseDatosSQL:
    def __init__(self, user: str, password: str):
        self.connection = pymysql.connect(
            host="localhost",
            port=3306, user=user,
            passwd=password,
            db="objetoSeguro")
        self.cursor = self.connection.cursor()

    def inserta_dato(self):
        sql = "INSERT INTO clientes VALUES (%s, %s)"
        self.cursor.execute(sql, ("Recursos", "Python"))
        # Guarda cambios
        self.connection.commit()
        self.connection.close()

    def muestra_bd(self):
        with self.connection.cursor() as cursor:
            sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            cursor.execute(sql, ('webmaster@python.org',))
            result = cursor.fetchone()
            print(result)


if __name__ == '__main__':
    bd = BaseDatosSQL("Nay", "pass")
    # mycursor.execute("CREATE DATABASE mydatabase")
    #bd.inserta_dato()

