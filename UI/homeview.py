import flet as ft

from database.course_DTO import CourseDTO

@ft.control
class HomeView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Lab O5 - segreteria studenti"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None

        # graphical elements
        self._title = None
        self.txt_name = None
        self.btn_hello = None
        self.txt_container = None
        self.course_dropdown = None
        self.results_list = None

    def load_interface(self):
        """Function that loads the graphical elements of the view"""
        # title
        self._title = ft.Text("App Gestione Studenti", color="blue", size=24)
        self._page.controls.append(self._title)
        self._page.on_close = self.controller.handle_close

        #ROW with some controls
        # text field for the name
        self.txt_name = ft.TextField(
            label="name",
            width=200,
            hint_text="Insert a your name"
        )

        self.course_dropdown = ft.Dropdown(
            width = 500,
            label = "Corso",
            hint_text = "Selezionare un corso",
            options= HomeView.__map_course_to_option__(self.controller.handle_load_courses_list())
        )
        self._page.controls.append(ft.Row(
            controls= [
                self.course_dropdown,
                ft.Button(
                    content="Cerca iscritti",
                    on_click=self.controller.handle_search_subscribers
                )
            ]
        ))

        self.results_list = ft.ListView(
                height=300,
                auto_scroll=True,
            controls=[
                ft.Text("Ciao"),
                ft.Text("Ciao"),
            ])

        self._page.controls.append(ft.Container(
            border=ft.Border.all(2, ft.Colors.BLACK),
            padding=10,
            content=ft.Column(controls= [self.results_list])
        ))

        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    @staticmethod
    def __map_course_to_option__(courses: list[CourseDTO]) -> list[ft.DropdownOption]:
        """Maps a list of courses (retrieved from the db to a map of controls for the UI"""
        return list(map(lambda course: ft.DropdownOption(
            key=course.codins,
            content=ft.Text(value=course.__str__())
        ), courses))

    def create_alert(self, message):
        """Function that opens a popup alert window, displaying a message
        :param message: the message to be displayed"""
        dlg = ft.AlertDialog(title=ft.Text(message, color=ft.Colors.RED))
        self._page.show_dialog(dlg)
        self._page.update()

    def update_page(self):
        self._page.update()
