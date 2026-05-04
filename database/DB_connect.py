import mysql.connector
from mysql.connector import errorcode

def get_connection() -> mysql.connector.connection:
    try:
        cnx = mysql.connector.connect(
            option_files='./secrets/connection.cnf'
        )
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return None
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return None
        else:
            print(err)
            return None


class DBConnect:
    """Unique class to handle database connections"""
    __connection__ = None

    def __init__(self):
        raise NotImplementedError("This is a singleton, do not instanciate")

    @classmethod
    def connect(cls) -> mysql.connector.connection:
        if cls.__connection__ is not None:
            return cls.__connection__

        else:
            cls.__connection__ = get_connection()
            return cls.__connection__

    @classmethod
    def close(cls):
        if cls.__connection__ is not None:
            cls.__connection__.close()
