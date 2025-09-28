

# 🎬 AuthService

![GitHub Repo Size](https://img.shields.io/github/repo-size/ArturRabello/AuthService?style=for-the-badge) ![Linguagens](https://img.shields.io/github/languages/count/ArturRabello/AuthService?style=for-the-badge&logoWidth=40&labelWidth=100)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) ![openapi initiative](https://img.shields.io/badge/openapiinitiative-%23000000.svg?style=for-the-badge&logo=openapiinitiative&logoColor=white) ![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens) ![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

O AuthService é uma API de autenticação independente, responsável por gerenciar o acesso seguro dos usuários. Seu principal objetivo é permitir que cada usuário registre sua conta, faça login, atualize sua senha, visualize seu perfil e gerencie suas sessões de forma simples e confiável.

Por ser independente, o AuthService pode ser integrado a qualquer sistema ou aplicação de cinema, não estando limitado apenas ao CineKeep. Ele realiza operações essenciais como registro de usuários, validação de credenciais, geração de tokens de autenticação seguros usando JWT (JSON Web Tokens) e armazenamento criptografado de senhas, garantindo segurança contra acessos indevidos.

Essa funcionalidade torna o AuthService uma ferramenta flexível e reutilizável, permitindo que qualquer plataforma de filmes ou serviço similar ofereça autenticação segura e gerenciamento de usuários sem depender de uma implementação específica do CineKeep.

## 🎯 Propósito

Este projeto foi desenvolvido como parte do programa de **Pós-Graduação em Desenvolvimento Full Stack da PUC Rio**, tendo como objetivo principal a **consolidação prática de conceitos teóricos estudados durante o curso**.

O desenvolvimento dessa aplicação, me permitiu aprimorar as minhas habilidades com as arquiteturas de desenvolvimento de software, implantação de containers atravez do docker e uma maior aprofundamento da ferramenta React

A ideia desse projeto foi simular uma pequena arquitetura de microsserviços, onde cada API é independente e autônoma, ou seja, consegue viver e operar sem depender diretamente dos outros serviços.

## Diagrama

![alt text](./assets/diagrama.png)

## 🔗 Componentes do Projeto CineKeep

- **[CineKeep](https://github.com/ArturRabello/CineKeep)** → Aplicação front-end
- **[UserMovieService](https://github.com/ArturRabello/UserMovieService)** → Api responsável por armazenar e gerenciar os filmes avaliados/salvos pelos usuários.
- **[API OMDB](https://www.omdbapi.com/)** → Api responsavel por fornece os dados dos filmes. 


## 🚀 Tecnologias

- **Flask** (framework web)
- **PostgreSQL** (banco de dados relacional (via psycopg2))
- **JWT** (autenticação com tokens)
- **Marshmallow** (validação e serialização de dados)
-  **Flask-CORS** (abilitação de CORS)
- **Docker** (Container)
- **Flask-Smorest / OpenAPI / Swagger** (documentação da API)



## 🛠️ Como utilizar 

### 2️⃣Clone o repositório:
```bash
git clone https://github.com/ArturRabello/AuthService.git
```
### 3️⃣ Instale as dependências:

```bash
(env)$ pip install -r requirements.txt
```

### 4️⃣ Executar localmente com NPM

**OBS**:Para rodar a aplicação, é necessário criar manualmente a tabela no PostgreSQL., [instale aqui.](https://www.postgresql.org/download/)

O nome da tabela deve ser **users**

No arquivo **database.py** você deve subistituir:


```bash
    DataBase_Url = os.getenv("DATABASE_URL")
```
 Por: 
````Bash
    DATABASE_URL = "postgresql://[SEU_USUARIO]:[SUA_SENHA]@localhost:5432/[NOME_DO_BANCO]"
````

**Execute a API atráves do flask:**
```bash
(env)$ flask run --host 0.0.0.0 --port 5200
```
**Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor automaticamente após uma mudança no código fonte.**
```bash
(env)$ flask run --host 0.0.0.0 --port 5200 --reload
```

### 5️⃣ Execute em um container Docker
**Será necessario que você tenha o Docker Desktop instalado em sua maquina.**
- [Windows](https://docs.docker.com/desktop/setup/install/windows-install/)
- [Linux](https://docs.docker.com/desktop/setup/install/linux/)
- [Mac](https://docs.docker.com/desktop/setup/install/mac-install/)

**Caso seu sistema operacional seja Windows ou Mac, será necessário instalar o [WSL 2](https://learn.microsoft.com/pt-br/windows/wsl/install)**

#### DockerFile
O Dockerfile define como a aplicação Python será construída e executada.

- **Imagem base** → Python 3.13.3, que fornece todas as bibliotecas padrão do Python.

- **Diretório de trabalho** → /app, onde o código será copiado e executado.

- **Instalação de dependências** → pip instala todos os pacotes listados em requirements.txt sem cache, garantindo que a imagem fique leve.

- **Variáveis de ambiente** → definem a configuração do Flask (app, host, porta e modo de desenvolvimento).

- **CMD** → comando para iniciar o Flask quando o container subir.


**Eu recomendo utilizar esse dockerfile.**

```
FROM python:3.13.3

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
ENV FLASK_RUN_PORT=5200

CMD ["flask", "run"]
```

#### Docker Compose

O Docker Compose permite orquestrar múltiplos containers, incluindo o banco de dados e o AuthService.

- **db (Postgres)**

    - Imagem oficial do PostgreSQL 17.

    - Define usuário, senha e banco de dados.

    - Porta 5432 mapeada para acesso local.

    - Volume persistente para manter os dados mesmo que o container seja recriado.

- **web (AuthService)**

    - Constrói a imagem usando o Dockerfile local.

    - Porta 5200 exposta para acessar a API via navegador ou frontend.

    - Variável de ambiente DATABASE_URL conecta a aplicação ao Postgres.

    - depends_on garante que o banco de dados seja iniciado antes do serviço.

    - Volume mapeia a pasta local /app para dentro do container, facilitando alterações no código em tempo de execução.

```
services:
  db:
    image: postgres:17
    container_name: postgres_db_auth
    restart: always
    environment:
      POSTGRES_USER: postgres_db_auth
      POSTGRES_PASSWORD: postgres_db_auth
      POSTGRES_DB: postgres_db_auth
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  web:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: service_auth
    ports:
      - "5200:5200"
    environment:
      - DATABASE_URL=postgresql://postgres_db_auth:postgres_db_auth@db/postgres_db_auth
    depends_on:
      - db
    volumes:
      - ./app:/app
volumes:
  pgdata:
```
#### Construir a imagem e subir o container

**Controi a imagem**
```
docker compose build
```

**Cria containers (se não existirem) e sobe eles. Pode rebuildar imagens se necessário.**

```
docker compose up
```

**Inicia o container**
```
docker compose start
```

## 🔍 funcionalidades

**🔐 Autenticação com JWT:** O sistema possui um processo de login que utiliza JSON Web Token (JWT) para garantir segurança e confiabilidade. Após a autenticação, um cookie é gerado e enviado ao navegador, permitindo que o usuário navegue de forma autenticada durante toda a sessão.

**Users**
- **Registra usuário** - POST /auth/register
- **Realiza login** - POST /auth/login
- **Verifica se o usuário está logado / retorna o usuário** - POST /auth getCurrentUser
- **Lista todos os usuários** - GET /auth/listUsers
- **Deletar usuário** - DELETE /auth/deleteUser
- **Atualizar senha** - PUT /auth/updatePassword
- **Deslogar** - POST /auth/logout

## 📂 Estrutra do projeto

```
📦 AuthService - Back-end
├── 📂 app
│   ├── ⚙️ app.py              → Arquivo principal da aplicação Flask
│   ├── ⚙️ database.py         → Configuração do banco de dados e conexão via SQLAlchemy
│   ├── ⚙️ models.py           → Modelos de dados (ex: User)
│   ├── ⚙️ schemas.py          → Esquemas de validação e serialização (Marshmallow)
│   ├── ⚙️ token_services.py   → Serviços de geração e validação de tokens JWT
│   └── 📂 __pycache__         → Arquivos compilados automaticamente pelo Python
├── 🐳 docker-compose.yml      → Orquestração dos containers (Flask + PostgreSQL)
├── 🐳 Dockerfile              → Instruções para build da imagem Docker do serviço
├── 📜 requirements.txt        → Dependências do projeto (Flask, SQLAlchemy, JWT, etc)
└── 📌 README.md               → Documentação geral do projeto
```
## 📌 Documentação da API – Auth Service

### 🔹 Registrar Usuário
```bash
POST /auth/register
```
| Parâmetro         | Tipo     | Descrição |
|-------------------|----------|------------|
| `userName`        | string   | **Obrigatório.** Nome de usuário (mínimo 3 e máximo 20 caracteres) |
| `email`           | string   | **Obrigatório.** Email válido |
| `password`        | string   | **Obrigatório.** Senha (mínimo 8 caracteres) |
| `passwordConfirm` | string   | **Obrigatório.** Confirmação da senha |

**Respostas:**
| Código | Descrição |
|--------|------------|
| 201 | Usuário registrado com sucesso |
| 400 | Dados inválidos |
| 409 | Email já existe |
| 422 | Senhas não coincidem |
| 500 | Erro no banco de dados |

---

### 🔹 Login
```bash
POST /auth/login
```
| Parâmetro   | Tipo   | Descrição |
|-------------|--------|------------|
| `email`     | string | **Obrigatório.** Email do usuário |
| `password`  | string | **Obrigatório.** Senha do usuário |

**Respostas:**
| Código | Descrição |
|--------|------------|
| 200 | Login realizado com sucesso (retorna token em cookie) |
| 401 | Senha inválida |
| 404 | Usuário não encontrado |
| 500 | Erro no banco de dados |

---

### 🔹 Obter Usuário Logado
```bash
POST /auth/getCurrentUser
```

**Requer cookie com `token` válido.**

**Respostas:**
| Código | Descrição |
|--------|------------|
| 200 | Retorna dados do usuário logado |
| 401 | Token inválido |
| 403 | Token não encontrado |
| 404 | Usuário não encontrado |
| 400 | Erro de validação |

---

### 🔹 Listar Usuários
```bash
GET /auth/listUsers
```

**Respostas:**
| Código | Descrição |
|--------|------------|
| 200 | Retorna lista de usuários |
| 404 | Nenhum usuário encontrado |
| 400 | Erro de validação |

---

### 🔹 Deletar Usuário
```bash
DELETE /auth/deleteUser
```

**Requer cookie com `token` válido.**

**Respostas:**
| Código | Descrição |
|--------|------------|
| 200 | Usuário deletado com sucesso (remove cookie `token`) |
| 401 | Token inválido |
| 403 | Token não encontrado |
| 404 | Usuário não encontrado |
| 400 | Erro de validação |

---

### 🔹 Atualizar Senha
```bash
PUT /auth/updatePassword
```
| Parâmetro    | Tipo   | Descrição |
|--------------|--------|------------|
| `email`      | string | **Obrigatório.** Email do usuário |
| `userName`   | string | **Obrigatório.** Nome do usuário |
| `newPassword`| string | **Obrigatório.** Nova senha |

**Respostas:**
| Código | Descrição |
|--------|------------|
| 200 | Senha atualizada com sucesso |
| 404 | Usuário não encontrado |
| 400 | Erro de validação |

---

### 🔹 Logout
```bash
POST /auth/logout
```

**Respostas:**
| Código | Descrição |
|--------|------------|
| 200 | Logout realizado com sucesso (remove cookie `token`) |
| 500 | Falha ao realizar logout |
