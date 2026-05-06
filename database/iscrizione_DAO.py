from mysql.connector import DatabaseError

from database.DB_connect import DBConnect
from database.StudentDAO import StudentDAO


class IscrizioneDAO:
    def __init__(self):
        raise NotImplementedError("This is a singleton")

    @staticmethod
    def get_subscription(student_id: int, course_id: str) -> bool:
        f"""Check if a specific student is subscribed to a specific course. 
        @returns True if the student is subscribed to the course, False otherwise
        @raises {DatabaseError} if there are multiple subscriptions for the same student at the same course. """

        cnx = DBConnect.connect()
        cursor = cnx.cursor(dictionary=True)

        query = """SELECT * FROM iscrizione WHERE matricola=%s AND codins=%s;"""
        data = (student_id, course_id)
        cursor.execute(query, data)
        res = cursor.fetchAll()
        cursor.close()

        if len(res) == 0:
            return False
        elif len(res) == 1:
            return True
        else:
            raise DatabaseError("Multiple subscriptions for the same student in the same course")

    @staticmethod
    def subscribe_student_to_course(student_id: int, course_id: str):
        if StudentDAO.get_student_by_id(int(student_id)) is None:
            raise ValueError(f"La matricola {student_id} non risulta nel database")

        if IscrizioneDAO.get_subscription(student_id, course_id):
            raise ValueError(f"Lo studente {student_id} è già iscritto al corso {course_id}")

        cnx = DBConnect.connect()
        cursor = cnx.cursor()
        query = """INSERT INTO iscrizione VALUES (%s, %s);"""

        data = (student_id, course_id)
        cursor.execute(query, data)
        cnx.commit()
        cursor.close()
