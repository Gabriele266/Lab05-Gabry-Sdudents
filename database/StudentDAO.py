from database.DB_connect import DBConnect
from database.student_DTO import StudentDTO


class StudentDAO:
    @classmethod
    def get_student_by_id(cls, matricola: int) -> StudentDTO | None:
        """Get detailed student informations by id if exists"""
        cnx = DBConnect.connect()
        cursor = cnx.cursor(dictionary=True)

        query = ("""SELECT * FROM studente 
                   WHERE matricola = %s;""")

        params = (matricola,)
        cursor.execute(query, params)

        all_res = cursor.fetchall()
        cursor.close()

        if len(all_res) > 0:
            row = all_res[0]
            return StudentDTO(matricola=row["matricola"],
                              cognome=row["cognome"],
                              nome=row["nome"],
                              cds=row["CDS"],
                              )
        else:
            return None