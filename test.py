import unittest

from database.StudentDAO import StudentDAO
from database.course_DAO import CourseDAO

class MyTestCase(unittest.TestCase):
    def test_search_by_id(self):
        r = StudentDAO.get_student_by_id(155459)

        self.assertIsNotNone(r)
        self.assertEqual(r.nome, "MARCO")
        r2 = StudentDAO.get_student_by_id(-2454564)
        self.assertIsNone(r2)

    def test_get_subscribers(self):
        r = CourseDAO.get_subscribers_to_course("01KSUPG")

        self.assertIsNotNone(r)
        self.assertIsInstance(r, set)
        r2 = CourseDAO.get_subscribers_to_course("MIANONNA")
        self.assertEqual(len(r2), 0)
        self.assertIsNotNone(r2)

if __name__ == '__main__':
    unittest.main()