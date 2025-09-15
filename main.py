from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

from database import init_db
from livro import (
    adicionar_livro, listar_livros, buscar_livros,
    atualizar_status, excluir_livro, formatar_livro,
    Categoria, Status
)

app = FastAPI(title="API da Biblioteca", description="Sistema de gerenciamento de biblioteca")

@app.on_event("startup")
def startup_event():
    init_db()
    print("Banco de dados inicializado com sucesso!")

class CategoriaEnum(int, Enum):
    romance = 1
    acao = 2
    ficcao = 3
    comedia = 4
    suspense = 5
    terror = 6
    outros = 99

class StatusEnum(int, Enum):
    ativo = 1
    inativo = 2
    excluido = 9

class LivroCreate(BaseModel):
    titulo: str
    autor: str
    editora: str
    categoria: CategoriaEnum
    ano: int

class LivroUpdateStatus(BaseModel):
    status: StatusEnum

class LivroResponse(BaseModel):
    id: int
    titulo: str
    autor: str
    editora: str
    categoria: int
    ano: int
    disponivel: bool
    status: int

    class Config:
        from_attributes = True

@app.post("/livros/", response_model=dict, summary="Adicionar um novo livro")
def criar_livro(livro: LivroCreate):
    try:
        livro_id = adicionar_livro(
            livro.titulo,
            livro.autor,
            livro.editora,
            livro.categoria,
            livro.ano
        )
        return {"message": "Livro adicionado com sucesso.", "livro_id": livro_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao adicionar livro: {str(e)}")

@app.get("/livros/", response_model=List[LivroResponse], summary="Listar todos os livros")
def listar_todos_os_livros():
    try:
        livros = listar_livros()
        return [formatar_livro(livro) for livro in livros]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar livros: {str(e)}")

@app.get("/livros/buscar", response_model=List[LivroResponse], summary="Buscar livros")
def buscar_livros_por_termo(termo: str):
    try:
        livros = buscar_livros(termo)
        return [formatar_livro(livro) for livro in livros]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar livros: {str(e)}")

@app.put("/livros/{livro_id}/status", response_model=dict, summary="Atualizar status do livro")
def atualizar_status_livro(livro_id: int, update: LivroUpdateStatus):
    try:
        if atualizar_status(livro_id, update.status):
            return {"message": "Status do livro atualizado com sucesso."}
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar status: {str(e)}")

@app.delete("/livros/{livro_id}", response_model=dict, summary="Excluir um livro")
def excluir_livro_endpoint(livro_id: int):
    try:
        if excluir_livro(livro_id):
            return {"message": "Livro excluído com sucesso."}
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao excluir livro: {str(e)}")

@app.get("/", include_in_schema=False)
def menu():
    return {
        "message": "Bem-vindo à API da Biblioteca",
        "endpoints": {
            "Adicionar livro": "POST /livros/",
            "Listar livros": "GET /livros/",
            "Buscar livros": "GET /livros/buscar?termo=...",
            "Atualizar status": "PUT /livros/{id}/status",
            "Excluir livro": "DELETE /livros/{id}"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)