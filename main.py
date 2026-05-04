import flet as ft

from model.model import Model
from UI.homeview import HomeView
from UI.controller import Controller


def main(page: ft.Page):
    my_model = Model()
    my_view = HomeView(page)
    my_controller = Controller(my_view, my_model)
    my_view.set_controller(my_controller)
    my_view.load_interface()


ft.app(target=main)
