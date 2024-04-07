# FastAPI Workout Management API

Este projeto consiste em uma API desenvolvida com FastAPI para gerenciar centros de treinamento de CrossFit, permitindo criar novos centros, cadastrar atletas, categorias e associar atletas aos centros de treinamento.

O desenvolvimento deste projeto faz parte do desafio do Módulo "Desenvolvendo sua primeira API com FastAPI e Python + Docker", como parte do bootcamp DIO Coding the Future - Vivo.

## Instalação e Execução

Para executar este projeto localmente, siga os passos abaixo:

1. **Clonar o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio

2. **Instalação das dependencias**

   ```bash
   pip install fastapi uvicorn[standard] pydantic sqlite-utils
   cd nome-do-repositorio

3. **Instalação do banco de dados**

    O projeto utiliza um banco de dados SQLite local. Não é necessário configurar nenhum servidor de banco de dados adicional.

    O projeto inicialmente elaborado pelo instrutor envolve usar o POSTGRES e o Docker. Entretanto, aulas anteriores do projeto não apresentaram de forma completa tais tecnologias. Dessa forma, decidi por simplificar o projeto usando SQLite. De modo que futuramente, irei refazer o projeto usando Docker e POSTGRES.

4. **Execução do projeto**

    ```bash
    uvicorn main:app --reload --port 8080

## Endpoints

    POST /atletas/: Cria um novo atleta.
    PUT /atletas/{atleta_id}: Atualiza os dados de um atleta existente.
    POST /categorias/: Cria uma nova categoria.
    POST /centros_treinamento/: Cria um novo centro de treinamento.
    POST /atletas/{atleta_id}/associar_centro/{centro_id}: Associa um atleta a um centro de treinamento.
    GET /centros_treinamento/{centro_id}/atletas: Obtém todos os atletas associados a um centro de treinamento específico.

## Exemplos

1. **POST /atletas/**

    ```bash
    {
        "nome": "Maria",
        "peso": 60.5,
        "altura": 1.65,
        "idade": 25,
        "sexo": "F",
        "cpf": "1",
        "telefone": "+5511999999998",
        "categoria_id": 1,
        "centro_treinamento_id": 1
    }
    ```

    Retorno:

    ```bash
    {
        "nome": "Maria",
        "peso": 60.5,
        "altura": 1.65,
        "idade": 25,
        "sexo": "F",
        "cpf": "2",
        "telefone": "+5511999999998",
        "id": 3,
        "categoria_id": 1
    }
    ```


2. **PUT /atletas/{atleta_id}**

    ```bash
    {
        "nome": "João",
        "peso": 60.5,
        "altura": 1.65,
        "idade": 25,
        "sexo": "F",
        "cpf": "2",
        "telefone": "+5511999999998",
        "categoria_id": 1,
        "centro_treinamento_id": 1
    }
    ```

    Retorno:

    ```bash
    {
	    "message": "Atleta com ID 3 atualizado com sucesso"
    }
    ```

3. **POST /categorias/**

    ```bash
    {
        "nome": "peso pena"
    }
    ```
    Retorno:

    ```bash
    {
        "nome": "peso pena",
        "id": 1,
        "centros_treinamento": []
    }
    ```

4. **POST /centros_treinamento/**

    ```bash
    {
        "nome": "GYM",
        "endereco": "Rua x, 002",
        "proprietario": "Fulaninho"
    }
    ```
    Retorno:

    ```bash
    {
        "nome": "GYM",
        "endereco": "Rua x, 002",
        "proprietario": "Fulaninho",
        "id": 2,
        "atletas": []
    }
    ```

5. **POST /atletas/{atleta_id}/associar_centro/{centro_id}**

    Retorno
    ```bash
    {
        "message": "Atleta 1 associado ao Centro de Treinamento 1"
    }
    ```

6. **GET /centros_treinamento/{centro_id}/atletas**

    Retorno
    ```bash
    [
        {
            "nome": "Maria",
            "peso": 60.5,
            "altura": 1.65,
            "idade": 25,
            "sexo": "F",
            "cpf": "12345678900",
            "telefone": "+5511999999999",
            "id": 1,
            "categoria_id": 1
        }
    ]
    ```
    

## Observações
O CPF e o telefone dos atletas são únicos, garantindo que não haja duplicação de dados.
O projeto utiliza SQLite como banco de dados local para armazenar os dados dos atletas, categorias e centros de treinamento.

