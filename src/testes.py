from data.database import MassesDatabase
from data.db_manager import DbManager
from ui.interface import UI
from application.app import App
import random
import flet as ft



def main(page: ft.Page):
    random.seed(1)
    memory_db = MassesDatabase("..\\database\\masses.db")
    db_manager = DbManager(memory_db)

    # products = [
    #     ('pizza calabresa com chocolate branco', 'pizza'),
    #     ('empadão camarão', 'empadão'),
    #     ('bolo morango', 'bolo'),
    #     ('pão doce', 'pão'),
    #     ('pizza camarão', 'pizza'),
    #     ('empadão calabresa', 'empadão')
    # ] 
    clients = ['marcos viagra', 'antonio cerraria', 'antonioato', 'migalha viagra']

    # for p in products:
    #     db_manager.add_product(
    #         p[0], p[1],
    #         round(random.randint(1,5) + random.random(), 2),
    #         round(random.randint(5,10) + random.random(), 2),
    #         random.randint(5,15)
    #     )

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.snack_bar = ft.SnackBar(content=ft.Text("", size=20), duration=1000)

    ui = UI(App(db_manager))
    page.add(ui)
    ui.start()


ft.app(target=main)
