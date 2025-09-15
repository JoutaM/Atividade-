from enum import Enum
from typing import List
import sqlite3
from database import conectar


class Categoria(Enum):
    romance = 1
    acao = 2
    ficcao = 3
    comedia = 4
    suspense = 5
    terror = 6
    outros = 99


class Status(Enum):
    ativo = 1
    inativo = 2
    excluido = 9


def adicionar_livro(titulo: str, autor: str, editora: str, categoria: int, ano: int) -> int:
    with conectar() as conn:
        cursor = conn.execute(
            ''' 
            INSERT INTO livros (titulo, autor, editora, categoria, ano, disponivel, livro_status) 
            VALUES (?, ?, ?, ?, ?, ?, ?) 
            ''',
            (titulo.strip(), autor.strip(), editora.strip(), int(categoria), ano, 1, Status.ativo.value)
        )
        conn.commit()
        return cursor.lastrowid


def listar_livros() -> List[sqlite3.Row]:
    with conectar() as conn:
        cursor = conn.execute(
            ''' 
            SELECT * FROM livros WHERE livro_status != ?;
            ''', (Status.excluido.value,)
        )
        return cursor.fetchall()


def buscar_livros(termo: str) -> List[sqlite3.Row]:
    like = f"%{termo.strip()}%"
    with conectar() as conn:
        cursor = conn.execute(
            ''' 
            SELECT * FROM livros 
            WHERE (lower(titulo) LIKE lower(?) 
                OR lower(autor) LIKE lower(?) 
                OR lower(editora) LIKE lower(?))
                AND livro_status != ?;
            ''', (like, like, like, Status.excluido.value)
        )
        return cursor.fetchall()


def atualizar_status(livro_id: int, status: int) -> bool:
    with conectar() as conn:
        cursor = conn.execute(
            ''' 
            UPDATE livros SET livro_status = ? WHERE id = ? 
            ''',
            (int(status), livro_id)
        )
        conn.commit()
        return cursor.rowcount > 0


def atualizar_disponibilidade(livro_id: int, disponivel: bool) -> bool:
    with conectar() as conn:
        cursor = conn.execute(
            ''' 
            UPDATE livros SET disponivel = ? WHERE id = ? 
            ''',
            (int(disponivel), livro_id)
        )
        conn.commit()
        return cursor.rowcount > 0


def excluir_livro(livro_id: int) -> bool:
    with conectar() as conn:
        cursor = conn.execute(
            ''' 
            UPDATE livros SET livro_status = ? WHERE id = ? 
            ''',
            (Status.excluido.value, livro_id)
        )
        conn.commit()
        return cursor.rowcount > 0


def formatar_livro(livro: sqlite3.Row) -> dict:
    return {
        "id": livro["id"],
        "titulo": livro["titulo"],
        "autor": livro["autor"],
        "editora": livro["editora"],
        "categoria": livro["categoria"],
        "ano": livro["ano"],
        "disponivel": bool(livro["disponivel"]),
        "status": livro["livro_status"]
    }