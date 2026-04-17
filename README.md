# SGAL - Subsistema de Gerenciamento de Ativos Literários

Projeto Flask para gerenciamento de inventário bibliográfico com arquitetura em camadas.

## Visão Geral

Este projeto implementa um CRUD básico de autores e livros usando:

- Flask
- Flask-SQLAlchemy
- Flask-Marshmallow
- Marshmallow-SQLAlchemy
- Flasgger
- Flask-Migrate
- Flask-CORS

A aplicação utiliza o padrão Application Factory e separação de responsabilidades entre:

- `app/models` → modelos de persistência
- `app/schemas` → serialização/deserialização
- `app/routes` → controladores e endpoints
- `app/database.py` → singleton do SQLAlchemy

## Estrutura do Projeto

```text
mission_control/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── models/
│   │   ├── author.py
│   │   └── book.py
│   ├── schemas/
│   │   └── library_schema.py
│   └── routes/
│       └── api_v1.py
├── config.py
├── requirements.txt
├── run.py
└── tests/
    └── test_app.py
```

## Como Executar

1. Ative o ambiente virtual:

```powershell
cd c:\Users\guilh\PROJETOS\gerenciamento-biblioteca
.\.venv\Scripts\Activate.ps1
```

2. Instale as dependências:

```powershell
cd mission_control
pip install -r requirements.txt
```

3. Execute a aplicação:

```powershell
python run.py
```

Depois disso, a API estará disponível em `http://127.0.0.1:5000`.

## Endpoints Principais

- `POST /api/v1/authors` → criar autor
- `GET /api/v1/authors` → listar autores com paginação
- `POST /api/v1/books` → criar livro
- `GET /api/v1/books` → listar livros com paginação

## Configuração

O projeto usa um arquivo `.env` para variáveis de ambiente. Esse arquivo não está rastreado pelo Git.

Variáveis suportadas:

- `DATABASE_URL` → string de conexão do SQLAlchemy
- `CORS_ORIGINS` → origens permitidas para CORS

## Observações

- `mission_control/.env` foi removido do controle de versão para proteger dados sensíveis.
- A API já possui validação de payload e tratamento de erros para `ValidationError` e `IntegrityError`.
- Foi fixado `Flask==2.2.5` para compatibilidade com `Flasgger`.

## GitHub

Repositório remoto sincronizado com:

https://github.com/guilhermemichael/gerenciamento-biblioteca.git
