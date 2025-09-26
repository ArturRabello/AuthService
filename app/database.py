
from datetime import time
import os
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import psycopg2

"""
    Configuração da base de dados
"""

# url do banco de dados
DataBase_Url = os.getenv("DATABASE_URL")
# Cria a engine do SQLAlchemy
engine = create_engine(DataBase_Url)
# Cria uma sessão ligada à engine
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Define a base declarativa para os modelos
Base = declarative_base()
# Cria todas as tabelas do banco definidas nos modelos
Base.metadata.create_all(bind=engine)