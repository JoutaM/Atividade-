import sqlite3

DB_NAME = "biblioteca.db"

def conectar() -> sqlite3.Connection:
    conn_db = sqlite3.connect(DB_NAME)
    conn_db.row_factory = sqlite3.Row
    return conn_db

def init_db():
    with conectar() as conn:
        conn.execute(
            ''' 
            CREATE TABLE IF NOT EXISTS livros ( 
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                titulo TEXT NOT NULL, 
                autor TEXT NOT NULL, 
                editora TEXT NOT NULL, 
                categoria INTEGER NOT NULL, 
                ano INTEGER, 
                disponivel INTEGER NOT NULL DEFAULT 1 CHECK (disponivel IN (0,1)), 
                livro_status INTEGER NOT NULL DEFAULT 1  
            ); 
            '''
        )
        conn.commit()