from os import environ
import mysql.connector as mariadb
from mysql.connector import Error


class MyDataBaseController:
    """DATABASE Controller"""

    def __init__(self, user: str, password: str, host: str, db_name: str, *models):
        """Constructor method

        :param user: User name
        :type user: str
        :param password: Password
        :type password: str
        :param host: Host or domain
        :type host: str
        :param db_name: DATABASE Name
        :type db_name: str
        :param models: DATABASE models
        """
        self.__create_database(user, password, host, db_name, *models)
        self.user = user
        self.__password = password
        self.host = host
        self.db_name = db_name

    def __create_database(
        self, user: str, password: str, host: str, db_name: str, *models
    ):
        """Create DATABASE

        :param user: User name
        :type user: str
        :param password: Password
        :type password: str
        :param host: Host or domain
        :type host: str
        :param db_name: DATABASE Name
        :type db_name: str
        :param models: DATABASE models
        """
        conn = mariadb.connect(user=user, password=password, host=host)
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        # Doping database MYDATABASE if already exists.
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")

        # Preparing query to create a database
        # sql = "CREATE DATABASE {db_name}";
        sql = f"CREATE DATABASE IF NOT EXISTS {db_name}"

        # Creating a database and tables
        cursor.execute(sql)
        cursor.execute(f"USE {db_name}")
        self.__create_tables(cursor, *models)
        cursor.fetchone()

        # Closing the connection
        conn.close()

    @staticmethod
    def __create_tables(cursor, *models):
        """Create Tables in DB

        :param cursor: cursos database
        :param models: table definition
        """
        for model in models:
            tb_name = list(model.keys())[0]
            table_sql = f"""CREATE TABLE {tb_name}(
                id int primary key not null auto_increment"""
            for field_name, field_type in model[tb_name].items():
                table_sql = table_sql + f", {field_name} {field_type}"
            try:
                cursor.execute(table_sql + ")")
            except Error as err:
                raise err

    def run_query(self, query: str, parameter=()):
        """Run SQL statement

        :param query: SQL statement
        :type query: str
        :param parameter: SQL statement parameters
        """
        conn = mariadb.connect(
            host=self.host,
            database=self.db_name,
            user=self.user,
            password=self.__password,
        )
        try:
            cursor = conn.cursor()
            cursor.execute(query, parameter)
            result = None
            if parameter:
                conn.commit()
            else:
                result = cursor.fetchall()
            return result
        except Error as err:
            raise err
        finally:
            conn.close()


if __name__ == "__main__":
    # * Table definition
    text_table = {"text": {"title": "varchar(30)", "content": "varchar(100)"}}

    # * Create database
    db_password = "passmaria"
    notes_db = MyDataBaseController("root", db_password, "localhost", "notes", text_table)

    # * Insert value in text table
    QUERY = "INSERT INTO text VALUES (Null, %s, %s)"
    values = ("my first text", "its note in mysql")
    notes_db.run_query(QUERY, values)

    # * Query to text table
    QUERY = "SELECT * FROM text"
    print(notes_db.run_query(QUERY))
