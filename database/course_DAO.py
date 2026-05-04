# Add whatever it is needed to interface with the DB Table corso

from database.DB_connect import get_connection
import mysql.connector

from database.StudentDAO import StudentDAO
from database.course_DTO import CourseDTO
from database.student_DTO import StudentDTO


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

    @classmethod
    def get_subscribers_to_course(cls, course_codins: str) -> set[StudentDTO]:
        """Returns a unique set of students who are subscribed to the course"""
        cnx = cls.connect()
        cursor = cnx.cursor()

        query = """SELECT * FROM iscrizione 
                   WHERE codins=%s;"""

        data = (course_codins,)
        cursor.execute(query, data)

        students = set()
        for (matricola, codins) in cursor:
            students.add(StudentDAO.get_student_by_id(matricola))

        cursor.close()
        cnx.close()

        return students
