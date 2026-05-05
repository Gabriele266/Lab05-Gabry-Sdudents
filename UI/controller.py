import flet as ft

from database.DB_connect import DBConnect
from database.StudentDAO import StudentDAO
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

    def handle_course_select(self, event):
        self._model.selected_course_code = event.data

    def handle_search_subscribers(self, event):
        cod_ins = self._model.selected_course_code

        if cod_ins is None or cod_ins == "":
            self._view.create_alert("Selezionare un corso")
            self._view.update_page()
            return

        res: set[StudentDTO] = CourseDAO.get_subscribers_to_course(cod_ins)
        self._view.results_list.controls = [ft.Container(
            margin=20,
            content=ft.Text(f"Ci sono {len(res)} iscritti al corso {cod_ins}", size=24, color=ft.Colors.BLUE, weight=ft.FontWeight.W_600))]       # clear controls

        for student in res:
            self._view.results_list.controls.append(ft.Text(f"{student.nome} {student.cognome} -- MATRICOLA {student.matricola}"))

        self._view.update_page()

    def handle_search_student_by_matricola(self, event):
        matricola = self._model.matricola_search

        if matricola is None or matricola == "":
            self._view.create_alert("Inserire una matricola")
            return

        if len(matricola) != 6:
            self._view.create_alert("La matricola deve essere un numero di 6 cifre")
            return

        result = StudentDAO.get_student_by_id(int(matricola))
        if result is None:
            self._view.create_alert("Nessuno studente esiste con quella matricola")
            return

        self._view.name_field.value = result.nome
        self._view.surname_field.value = result.cognome
        self._view.update_page()

    def handle_search_courses(self, event):
        matricola = self._model.matricola_search

        if matricola is None or matricola == "":
            self._view.create_alert("Inserire una matricola")
            return

        if len(matricola) != 6:
            self._view.create_alert("La matricola deve essere un numero di 6 cifre")
            return

        try:
            result = CourseDAO.get_courses_for_student(int(matricola))

            self._view.results_list.controls = [self._view.map_subscription_to_table(result)]
            self._view.update_page()
        except ValueError:
            self._view.create_alert(f"Lo studente {matricola} non risulta nel database")

    def handle_subscribe_student(self):
        pass


    def handle_change_matricola(self, e):
        self._model.matricola_search = e.data
        self._view.name_field.value = ""
        self._view.surname_field.value = ""

    def handle_close(self):
        print("Good bye")
        DBConnect.close()

    def handle_load_courses_list(self) -> list[CourseDTO]:
        return CourseDAO.get_available_courses()
