# Add whatever it is needed to interface with the DB Table corso

from database.DB_connect import DBConnect
from database.StudentDAO import StudentDAO
from database.course_DTO import CourseDTO
from database.student_DTO import StudentDTO

class CourseDAO:
    @classmethod
    def get_available_courses(cls) -> list[CourseDTO]:
        cnx = DBConnect.connect()

        cursor = cnx.cursor()
        query = """SELECT * FROM corso;"""

        cursor.execute(query)

        l = []
        for (codins, crediti, nome, pd) in cursor:
            l.append(CourseDTO(codins, crediti, nome, pd))

        cursor.close()
        return l

    @classmethod
    def get_subscribers_to_course(cls, course_codins: str) -> set[StudentDTO]:
        """Returns a unique set of students who are subscribed to the course"""
        cnx = DBConnect.connect()
        cursor = cnx.cursor(dictionary=True)

        query = """SELECT * FROM iscrizione 
                   WHERE codins=%s;"""

        data = (course_codins,)
        cursor.execute(query, data)

        students = set()
        for row in cursor.fetchall():
            students.add(StudentDAO.get_student_by_id(row["matricola"]))

        cursor.close()

        return students
