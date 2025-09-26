from datetime import datetime
from typing import Union
from database import Base
from sqlalchemy import Column, Date, Integer, String,Date
from werkzeug.security import generate_password_hash, check_password_hash
"""
     Modelo de usuário para o banco de dados usando SQLAlchemy.
"""
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    userName = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False)
    password_hash = Column(String(512), nullable=False)
    
    def __init__(self, userName, email):
        self.userName = userName
        self.email = email
    
    #função para criptografar a senha
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    #função para verificar se a senha esta correta
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

        
         
