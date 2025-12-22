from data.database import MassesDatabase
from data.db_manager import DbManager
from ui.interface import UI
from application.app import App
import random
import flet as ft



def main(page: ft.Page):
    memory_db = MassesDatabase("..\\database\\masses.db")
    db_manager = DbManager(memory_db)
    
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.snack_bar = ft.SnackBar(content=ft.Text("", size=20), duration=1000)

    ui = UI(App(db_manager))
    page.add(ui)
    ui.start()


ft.app(target=main)
