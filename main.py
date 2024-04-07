from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List
from sqlite3 import IntegrityError

# Definição dos modelos (schemas)
class AtletaBase(BaseModel):
    nome: str
    peso: float
    altura: float
    idade: int
    sexo: str
    cpf: str
    telefone: str

class AtletaCreate(AtletaBase):
    categoria_id: int  # ID da categoria à qual o atleta pertence

class Atleta(AtletaBase):
    id: int
    categoria_id: int  # ID da categoria à qual o atleta pertence

    class Config:
        orm_mode = True

class CategoriaBase(BaseModel):
    nome: str

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int
    centros_treinamento: List['CentroTreinamento'] = []  # Usando aspas simples para resolver o erro de nome

    class Config:
        orm_mode = True

class CentroTreinamentoBase(BaseModel):
    nome: str
    endereco: str
    proprietario: str

class CentroTreinamentoCreate(CentroTreinamentoBase):
    pass

class CentroTreinamento(CentroTreinamentoBase):
    id: int
    atletas: List[Atleta] = []  # Corrigindo o uso de List

    class Config:
        orm_mode = True

class AtletaUpdate(BaseModel):
    nome: str = None
    peso: float = None
    altura: float = None
    idade: int = None
    sexo: str = None
    cpf: str = None
    telefone: str = None
    categoria_id: int = None

# Criação da aplicação FastAPI
app = FastAPI()

# Função para criar uma nova conexão SQLite
def get_db_conn():
    return sqlite3.connect('workout.db')

# Criação das tabelas no banco de dados
def create_tables():
    conn = get_db_conn()
    c = conn.cursor()

    # Tabela Atleta
    c.execute("""
    CREATE TABLE IF NOT EXISTS atleta (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        peso REAL NOT NULL,
        altura REAL NOT NULL,
        idade INTEGER NOT NULL,
        sexo TEXT NOT NULL,
        cpf TEXT NOT NULL UNIQUE,  -- Garante que o CPF seja único
        telefone TEXT NOT NULL UNIQUE,  -- Garante que o telefone seja único
        categoria_id INTEGER,
        centro_treinamento_id INTEGER,
        FOREIGN KEY (categoria_id) REFERENCES categoria(id),
        FOREIGN KEY (centro_treinamento_id) REFERENCES centro_treinamento(id)
    )
    """)

    # Tabela Categoria
    c.execute("""
    CREATE TABLE IF NOT EXISTS categoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    """)

    # Tabela CentroTreinamento
    c.execute("""
    CREATE TABLE IF NOT EXISTS centro_treinamento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        endereco TEXT NOT NULL,
        proprietario TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

# Endpoint para criar um novo atleta
@app.post("/atletas/", response_model=Atleta)
def create_atleta(atleta: AtletaCreate):
    try:
        conn = get_db_conn()
        c = conn.cursor()
        c.execute("""
        INSERT INTO atleta (nome, peso, altura, idade, sexo, cpf, telefone, categoria_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (atleta.nome, atleta.peso, atleta.altura, atleta.idade, atleta.sexo, atleta.cpf, atleta.telefone, atleta.categoria_id))
        conn.commit()
        atleta_id = c.lastrowid
        return {**atleta.dict(), "id": atleta_id}
    except IntegrityError as e:
        if "UNIQUE constraint failed: atleta.cpf" in str(e):
            raise HTTPException(status_code=400, detail="CPF já cadastrado")
        elif "UNIQUE constraint failed: atleta.telefone" in str(e):
            raise HTTPException(status_code=400, detail="Telefone já cadastrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.put("/atletas/{atleta_id}")
def update_atleta(atleta_id: int, atleta_update: AtletaUpdate):
    try:
        conn = get_db_conn()
        c = conn.cursor()

        # Montar a string de UPDATE dinâmica com base nos campos fornecidos para atualização
        update_fields = []
        update_values = []

        if atleta_update.nome is not None:
            update_fields.append("nome = ?")
            update_values.append(atleta_update.nome)
        if atleta_update.peso is not None:
            update_fields.append("peso = ?")
            update_values.append(atleta_update.peso)
        if atleta_update.altura is not None:
            update_fields.append("altura = ?")
            update_values.append(atleta_update.altura)
        if atleta_update.idade is not None:
            update_fields.append("idade = ?")
            update_values.append(atleta_update.idade)
        if atleta_update.sexo is not None:
            update_fields.append("sexo = ?")
            update_values.append(atleta_update.sexo)
        if atleta_update.cpf is not None:
            update_fields.append("cpf = ?")
            update_values.append(atleta_update.cpf)
        if atleta_update.telefone is not None:
            update_fields.append("telefone = ?")
            update_values.append(atleta_update.telefone)
        if atleta_update.categoria_id is not None:
            update_fields.append("categoria_id = ?")
            update_values.append(atleta_update.categoria_id)

        if not update_fields:
            raise HTTPException(status_code=400, detail="Nenhum campo de atualização fornecido")

        # Montar a query SQL de UPDATE
        update_query = f"UPDATE atleta SET {', '.join(update_fields)} WHERE id = ?"
        update_values.append(atleta_id)

        # Executar a query de UPDATE
        c.execute(update_query, update_values)
        conn.commit()

        return {"message": f"Atleta com ID {atleta_id} atualizado com sucesso"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# Endpoint para criar uma nova categoria
@app.post("/categorias/", response_model=Categoria)
def create_categoria(categoria: CategoriaCreate):
    try:
        conn = get_db_conn()
        c = conn.cursor()
        c.execute("INSERT INTO categoria (nome) VALUES (?)", (categoria.nome,))
        conn.commit()
        categoria_id = c.lastrowid
        return {**categoria.dict(), "id": categoria_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# Endpoint para criar um novo centro de treinamento
@app.post("/centros_treinamento/", response_model=CentroTreinamento)
def create_centro_treinamento(centro: CentroTreinamentoCreate):
    try:
        conn = get_db_conn()
        c = conn.cursor()
        c.execute("""
        INSERT INTO centro_treinamento (nome, endereco, proprietario)
        VALUES (?, ?, ?)
        """, (centro.nome, centro.endereco, centro.proprietario))
        conn.commit()
        centro_id = c.lastrowid
        return {**centro.dict(), "id": centro_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.post("/atletas/{atleta_id}/associar_centro/{centro_id}")
def associar_atleta_centro(atleta_id: int, centro_id: int):
    try:
        # Lógica para associar o atleta ao centro de treinamento
        conn = get_db_conn()
        c = conn.cursor()
        c.execute("UPDATE atleta SET centro_treinamento_id = ? WHERE id = ?", (centro_id, atleta_id))
        conn.commit()
        return {"message": f"Atleta {atleta_id} associado ao Centro de Treinamento {centro_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/centros_treinamento/{centro_id}/atletas", response_model=List[Atleta])
def get_atletas_by_centro(centro_id: int):
    try:
        conn = get_db_conn()
        c = conn.cursor()
        c.execute("SELECT * FROM atleta WHERE centro_treinamento_id = ?", (centro_id,))
        atletas = c.fetchall()

        result = []
        for atleta in atletas:
            atleta_dict = {
                "id": atleta[0],
                "nome": atleta[1],
                "peso": atleta[2],
                "altura": atleta[3],
                "idade": atleta[4],
                "sexo": atleta[5],
                "cpf": atleta[6],
                "telefone": atleta[7],
                "categoria_id": atleta[8],
                "centro_treinamento_id": atleta[9]
            }
            result.append(atleta_dict)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


# Chamada para criar as tabelas ao iniciar o aplicativo
create_tables()

# Execução da aplicação com Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080, log_level='info', reload=True)
