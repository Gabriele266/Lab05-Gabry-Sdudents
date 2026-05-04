import mysql.connector
from database.DB_connect import get_connection
from database.student_DTO import StudentDTO


class StudentDAO:
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
    def get_student_by_id(cls, matricola: int) -> StudentDTO | None:
        """Get detailed student informations by id if exists"""
        cnx = cls.connect()
        cursor = cnx.cursor(dictionary=True)

        query = ("""SELECT * FROM studente 
                   WHERE matricola = %s;""")

        params = (matricola,)
        cursor.execute(query, params)

        all_res = cursor.fetchall()
        cursor.close()
        cnx.close()

        if len(all_res) > 0:
            row = all_res[0]
            return StudentDTO(matricola=row["matricola"],
                              cognome=row["cognome"],
                              nome=row["nome"],
                              cds=row["CDS"],
                              )
        else:
            return None