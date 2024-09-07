import mysql.connector
import mysql.connector.cursor
from mysql.connector.connection import MySQLConnection


class ClassConnection(MySQLConnection):
    """
    Class wrapper for MySQLConnection from mysql-connector

    Args:
        ClassConnection(MySQLConnection): connection database
    """

    _host = "localhost"
    _user = "root"
    _database = ""
    _password = ""
    _port = 3306
    _conn: mysql.connector.MySQLConnection = None
    _cursor: mysql.connector.cursor.MySQLCursor = None

    def __init__(
        self,
        host=_host,
        user=_user,
        database=None,
        password=_password,
        port=_port,
        **kwargs,
    ):
        """
        Get instance of ClassConnection

        Params: host, user, database, password, port

        Return: None
        """
        # Se kwargs for fornecido, ele sobrescreve os valores padrão
        if kwargs:
            self._host = kwargs.get("host", host)
            self._user = kwargs.get("user", user)
            self._nome = kwargs.get("database", database)
            self._password = kwargs.get("password", password)
            self._port = kwargs.get("port", port)
        else:
            self._host = host
            self._user = user
            self._nome = database
            self._password = password
            self._port = port

    def connected(self):
        """
        Get instance of MySQLConnection

        Returns:
        MySQLConnection: connect of database
        """

        configs = {
            "host": self._host,
            "user": self._user,
            "password": self._password,
            "port": self._port,
            "database": self._nome,
            "charset": "utf8mb4",
        }
        try:
            self._conn = mysql.connector.connect(**configs)
            return self._conn
        except mysql.connector.Error as err:
            print(f"Erro ao conectar: {err}")
            return None

    def get_cursor(self):
        """
        Get instance of MySQLCursor

        Returns:
        MySQLCursor: execute querys, updates, delete and any in database
        """
        if self._conn:
            self._cursor = self._conn.cursor()
            return self._cursor
        else:
            raise Exception("Conexão não estabelecida.")

    def desconected(self):
        """
        Close connection to the database and close the cursor

        Returns:
        Bool: False in case of exception | True in case of success
        """
        if self._conn:
            try:
                # Verifica se o cursor tem resultados pendentes e consome-os
                if self._cursor:
                    if self._cursor.with_rows:
                        self._cursor.fetchall()  # Ler todos os resultados pendentes
                    self._cursor.close()

                self._conn.close()
                return True
            except Exception as e:
                print(f"Erro ao fechar a conexão: {e}")
                return False
        return True

    def query(self, func):
        """
        Decorator to execute a function with a connection
        """

        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            finally:
                self.desconected()

        return wrapper

    def update(self, func):
        """
        Decorator to execute a function that updates the database
        """

        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
                self._conn.commit()
            finally:
                self.desconected()

        return wrapper
