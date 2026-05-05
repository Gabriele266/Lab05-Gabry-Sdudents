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
        self.name_field = None
        self.surname_field = None

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

        self.name_field = ft.TextField(read_only=True, label="Nome")
        self.surname_field = ft.TextField(read_only=True, label="Cognome")

        self._page.controls.append(ft.Row(
            controls= [
                ft.TextField(label="Matricola",
                             hint_text="Inserisci una matricola",
                             input_filter=ft.InputFilter(
                                 allow=False,
                                 regex_string=r"^\d{0,6}$"
                             ),
                             on_change=self.controller.handle_change_matricola),
                self.name_field,
                self.surname_field
            ]
        ))
        self._page.controls.append(ft.Row(
            controls = [
                ft.Button("Cerca studente", on_click=self.controller.handle_search_student_by_matricola),
                ft.Button("Cerca corsi", on_click=self.controller.handle_search_courses),
                ft.Button("Iscrivi studente al corso")
            ]
        ))

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

    @staticmethod
    def map_subscription_to_table(courses: list[CourseDTO]) -> ft.DataTable:
        """Map a list of courses (where the student is suscribed) to a table"""
        return ft.DataTable(
            columns=[
                ft.DataColumn(
                    label=ft.Text("Nome del corso")
                ),
                ft.DataColumn(
                    label=ft.Text("Codice del corso")
                ),
                ft.DataColumn(
                    label=ft.Text("CFU assegnati")
                ),
                ft.DataColumn(
                    label=ft.Text("Periodo didattico")
                )
            ],
            rows= [ft.DataRow(cells=[
                ft.DataCell(ft.Text(course.name)),
                ft.DataCell(ft.Text(course.codins)),
                ft.DataCell(ft.Text(str(course.credits))),
                ft.DataCell(ft.Text(str(course.pd))),
            ]) for course in courses ]
        )

    def create_alert(self, message):
        """Function that opens a popup alert window, displaying a message
        :param message: the message to be displayed"""
        dlg = ft.AlertDialog(title=ft.Text(message, color=ft.Colors.RED))
        self._page.show_dialog(dlg)
        self._page.update()

    def update_page(self):
        self._page.update()
