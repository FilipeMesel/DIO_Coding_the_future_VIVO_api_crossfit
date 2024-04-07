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


