from database import MassesDatabase
from db_manager import DbManager
import random
import datetime


m_db = MassesDatabase()
conn = m_db.get_connection()
cursor = conn.cursor()

products = [
    ('pizza calabresa', 'pizza'),
    ('empadão camarão', 'empadão'),
    ('bolo morango', 'bolo'),
    ('pão doce', 'pão'),
    ('pizza camarão', 'pizza'),
    ('empadão calabresa', 'empadão')
] 

clients = ['marcos viagra', 'antonio cerraria', 'antonioato', 'migalha viagra']

for p_name, p_type in products:
        m_db.add_product(
            cursor,
            p_name,
            p_type,
            round(random.randint(0,10) + random.random(), 2),
            round(random.randint(4,15) + random.random(), 2),
            random.randint(10,20),
        )

mdbm = DbManager(m_db)
print([tuple(item) for item in m_db.get_by_text(cursor, 'produtos', 'empadão')])
