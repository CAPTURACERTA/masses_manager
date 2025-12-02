from database import MassesDatabase
from db_manager import DbManager
import random
import flet as ft
from app import App


def main(page: ft.Page):
    random.seed(1)
    memory_db = MassesDatabase()
    db_manager = DbManager(memory_db)

    products = [
        ('pizza calabresa', 'pizza'),
        ('empadão camarão', 'empadão'),
        ('bolo morango', 'bolo'),
        ('pão doce', 'pão'),
        ('pizza camarão', 'pizza'),
        ('empadão calabresa', 'empadão')
    ] 
    clients = ['marcos viagra', 'antonio cerraria', 'antonioato', 'migalha viagra']

    for p in products:
        db_manager.add_product(
            p[0], p[1],
            round(random.randint(1,5) + random.random(), 2),
            round(random.randint(5,10) + random.random(), 2),
            random.randint(5,15)
        )

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(App(db_manager))


ft.app(target=main)
