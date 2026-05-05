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

    @classmethod
    def get_courses_for_student(cls, student_id: int) -> list[CourseDTO]:
        """Search all the courses that a student has been subscribed to"""

        # Verify if the student exists
        if StudentDAO.get_student_by_id(student_id) is None:
            raise ValueError("Student not found in the database")

        cnx = DBConnect.connect()
        cursor = cnx.cursor(dictionary=True)

        query = """SELECT * FROM iscrizione, corso
                WHERE matricola=%s AND iscrizione.codins=corso.codins;"""

        data = (student_id,)
        cursor.execute(query, data)
        l = []
        for row in cursor.fetchall():
            l.append(CourseDTO(codins=row["codins"],
                               credits=row["crediti"],
                               name=row["nome"],
                               pd=row["pd"]))

        cursor.close()
        return l