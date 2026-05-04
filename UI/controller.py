import flet as ft

from database.DB_connect import DBConnect
from database.course_DAO import CourseDAO
from database.course_DTO import CourseDTO
from database.student_DTO import StudentDTO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_hello(self, e):
        """Simple function to handle a button-pressed event,
        and consequently print a message on screen"""
        name = self._view.txt_name.value
        if name is None or name == "":
            self._view.create_alert("Inserire il nome")
            return
        self._view.txt_result.controls.append(ft.Text(f"Hello, {name}!"))
        self._view.update_page()

    def handle_search_subscribers(self, event):
        print("Search subscribers")
        codIns = self._view.course_dropdown.value

        if codIns is None:
            self._view.create_alert("Selezionare un corso")
            return

        print(codIns)
        res: set[StudentDTO] = CourseDAO.get_subscribers_to_course(codIns)
        self._view.results_list.controls = []       # clear controls

        for student in res:
            self._view.results_list.controls.append(ft.Text(f"{student.nome} {student.cognome} -- MATRICOLA {student.matricola}"))

        self._view.update_page()

    def handle_close(self):
        print("Good bye")
        DBConnect.close()

    def handle_load_courses_list(self) -> list[CourseDTO]:
        return CourseDAO.get_available_courses()
