import jwt
import datetime

SECRET_KEY = "chave_super_secreta" 

class Token:
  """
    Classe utilitária para gerar e decodificar tokens JWT para autenticação de usuários.
  """

  # Gera um token JWT para um usuário.
  @staticmethod
  def generate_token(user_id:int) -> str:
    
    now = datetime.datetime.now(datetime.timezone.utc)
    
    payload = {
      "user_id": user_id,
      "exp": now + datetime.timedelta(hours=3),
      "iat": now
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token
  
  # Decodifica um token JWT e retorna o payload.
  @staticmethod
  def decode_token(token:str) -> dict:
    try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
      return payload
    except jwt.ExpiredSignatureError:
      return {"message": "Token expirado"}
    except jwt.InvalidTokenError:
      return {"message": "Token inválido"}
