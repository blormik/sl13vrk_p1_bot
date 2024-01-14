import sqlite3
from sqlite3 import Error
path = r'db.sqlite'
print(f"Путь к БД: '{path}'")

def create_connection():
    connection = None
    try:
        connection = sqlite3.connect(path, check_same_thread=False)
        print("Подключение к БД SQLite прошло успешно")
        return connection        
    except Error as error:
        print(f"Произошла ошибка подключения к БД '{error}'")

conn = create_connection()

def create_table(query):
    try:
        ccursor = conn.cursor()
        ccursor.execute(query)
        conn.commit()        
    except Error as error:
        print(error)

def update(query, row):
    try:
        cursor = conn.cursor()
        cursor.execute(query, row)
        conn.commit()
    except Error as error:
        print("Failed to update sqlite table", error)

def insert(query, row):
    try:
        cursor = conn.cursor()
        cursor.execute(query, row)
        conn.commit()
        return cursor.lastrowid        
    except Error as error:
        print("Failed to insert sqlite table", error)

def delete(query, id):
    try:
        cursor = conn.cursor()
        cursor.execute(query, id)
        conn.commit()
    except Error as error:
        print("Failed to delete sqlite table", error)

def select(query, row):
    try:
        cursor = conn.cursor()
        cursor.execute(query, row)
        rows = cursor.fetchall()
        return rows        
    except Error as error:
        print("Failed to select sqlite table", error)

def is_table_exist(table_name):
    result = False
    try:
        cursor = conn.cursor()
        query = ''' select count(id) from ''' + table_name
        cursor.execute(query)
        if cursor.fetchone()[0] == 1: 
            result = True
        return result            
    except Error as error:
        print("Failed to check sqlite table2", error)
    
