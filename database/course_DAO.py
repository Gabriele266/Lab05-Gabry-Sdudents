# Add whatever it is needed to interface with the DB Table corso

from database.DB_connect import get_connection
import mysql.connector

from database.course_DTO import CourseDTO


class CourseDAO:
    __connection__ = None

    def __init__(self):
        raise NotImplementedError("This is a singleton, do not instanciate")

    @classmethod
    def connect(cls) -> mysql.connector.connection:
        if CourseDAO.__connection__ is not None:
            return CourseDAO.__connection__

        else:
            cls.__connection__ = get_connection()
            return cls.__connection__

    @classmethod
    def get_available_courses(cls) -> list[CourseDTO]:
        cnx = cls.connect()

        cursor = cnx.cursor()
        query = """SELECT * FROM corso;"""

        cursor.execute(query)

        l = []
        for (codins, crediti, nome, pd) in cursor:
            l.append(CourseDTO(codins, crediti, nome, pd))

        cursor.close()
        cnx.close()
        return l