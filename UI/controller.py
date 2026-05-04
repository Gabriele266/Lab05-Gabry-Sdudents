import flet as ft

from database.course_DAO import CourseDAO
from database.course_DTO import CourseDTO


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

    def handle_load_courses_list(self) -> list[CourseDTO]:
        return CourseDAO.get_available_courses()
