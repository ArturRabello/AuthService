from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from marshmallow import ValidationError
from flask_smorest import Api, Blueprint
from sqlalchemy.exc import IntegrityError, OperationalError
from database import Base, Session, engine
from sqlalchemy.exc import SQLAlchemyError
from models import  User
from schemas import *
from token_services import Token 
import jwt
import datetime
import re


#define o app flask e o formato da documentação da API
app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])
app.config["API_TITLE"] = "auth Service"
app.config["API_VERSION"] = "1.0"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
api = Api(app)

#define o blueprint, é ela que organiza as rotas e a documentação
auth_db = Blueprint('Auth', 'auth', url_prefix="/auth",description="Autenticação de usuário")

#atraves do Base definido no database.py cria as tabelas
Base.metadata.create_all(bind=engine)

"""
    Rota para o registro de um novo usuário.
    utiliza o set_password para criptografar a senha do usuário antes de salvar no banco.
"""
@auth_db.route('/register', methods=['POST'])
@auth_db.arguments(UserRegisterSchema)
@auth_db.response(201, responseUserSchema, description="User registered successfully")
@auth_db.response(400, errorInvalidRequestDataSchema,  description="Validation error")
@auth_db.response(422, errorPasswordNotMatchSchema, description="Passwords do not match")
@auth_db.response(409, errorEmailAlreadyExistsSchema, description="Email already exists")
@auth_db.response(500, errorDatabaseErrorSchema, description="Database error")
def register(user_data):
    patternEmail = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    patternUserName = r'^[A-Za-z0-9_.]+$'


    if (not user_data['userName'].strip() and
    not user_data['email'].strip() and
    not user_data['password'].strip() and
    not user_data['passwordConfirm'].strip()):
        return jsonify({"message": "All fields are required."}), 400

    # validação UserName
    if not (user_data['userName']).strip():
        return jsonify({"message": "User name is required."}), 400
    if len(user_data['userName']) < 3 or len(user_data['userName']) > 20:
        return jsonify({"message": "User name must be at least 3 characters and at most 20 characters."}), 400
    if not re.match(patternUserName, user_data['userName']):
        return jsonify({"message": "User name must only contain letters, numbers, sand underscores."}), 400

    # validação Email
    if user_data['email'].strip() == "":
        return jsonify({"message": "Email is required."}), 400
    if not re.match(patternEmail, user_data['email']):
        return jsonify({"message": "Invalid email format."}), 400

    # validação Senha
    if not (user_data['password']).strip():
        return jsonify({"message": "Password is required."}), 400
    if len(user_data['password']) < 8:
        return jsonify({"message": "Password must be at least 8 characters."}), 400
    if  user_data['password'] != user_data['passwordConfirm']:
        return jsonify({"message": "Passwords do not match."}), 422

    user = User(
        userName = user_data['userName'],
        email = user_data['email'],
    )
    
    user.set_password(user_data['password'])

    try:
        session = Session()
        
        if session.query(User).filter(User.email == user.email).first():
            session.close()
            return jsonify({"message": "Email already exists."}), 409
        session.add(user)
        session.commit()        
        return jsonify({"message": "User registered successfully"}), 201     
    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400        
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"message": "Database error", "error": str(e)}), 500
    finally:
        if session:
            session.close()
       
"""
    Rota de login, verifica se o usuario existe e se a senha esta correta
    utiliza o check_password para verificar se a senha esta correta, atraves de um hash criptografado
    retorna um token de autenticacao
"""     
            
@auth_db.route('/login', methods=['POST'])
@auth_db.arguments(UserLoginSchema)
@auth_db.response(200,errorLoginSchema, description="Login successful")
@auth_db.response(401,errorUserNotFoundSchema, description="Invalid password")
@auth_db.response(404,erroInvalidPasswordSchema, description="User not found")
def login(user_data):
    session = Session()
    if(user_data['email'].strip() == "" or user_data['password'].strip() == ""):
        return jsonify({"message": "All fields are required."}), 400
    try:
        user = session.query(User).filter_by(email=user_data['email']).first()
        if not user:
            session.close()
            return jsonify({"message": "User not found."}), 404
        
        if user.check_password(user_data['password']):
            token = Token.generate_token(user.id)

            payload = jwt.decode(token, options={"verify_signature": False})
            exp_time = payload["exp"]

            exp_time = datetime.datetime.fromtimestamp(payload["exp"], tz=datetime.timezone.utc)
            max_age = (exp_time - datetime.datetime.now(datetime.timezone.utc)).total_seconds()

            response = make_response(jsonify({"message": "Login successful"}))
            response.set_cookie("token", token, httponly=True, samesite='None', max_age=max_age, secure=True)
            return response, 200
        else:
            session.close()
            return jsonify({"message": "Invalid password"}), 401
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"message": "Database error", "error": str(e)}), 500
    finally:
        if session:
            session.close()

"""
    Rota para verificar se o usuario esta logado
"""
            
@auth_db.route('/getCurrentUser', methods=['POST'])
@auth_db.response(200, UserSchemaResponseSchema, description="Users")
@auth_db.response(400, errorInvalidRequestDataSchema, description="Validation error")
@auth_db.response(404, errorUserNotFoundSchema, description="User not found")
def list_user():
    session = Session()
    try:
        token = request.cookies.get('token') 

        if not token:
            return jsonify({"message": "Token not found."}), 403

        payload = Token.decode_token(token)
        if "message" in payload:
            return jsonify(payload.get("message")), 401

        user_id = payload["user_id"]
        users = session.query(User).filter(User.id == user_id).first()
        session.close()
        if users:
            return jsonify(returnUser(users)), 200
        else:
            return jsonify({"message": "User not found."}), 404
    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400
    finally:
        if session:
            session.close()

"""
    Rota para listar todos os usuarios
"""

@auth_db.route('/listUsers', methods=['GET'])
@auth_db.response(200, UserListSchema, description="List of users")  
@auth_db.response(400, errorInvalidRequestDataSchema, description="Validation error")
@auth_db.response(404, errorUserNotFoundSchema, description="User not found")
def list_users():
    session = Session()
    try:
        users = session.query(User).all()
        session.close()
        if users:
            return jsonify(returnUserList(users)), 200
        else:
            return {"message": "User not found."}, 404     
    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400
    finally:
        if session:
            session.close()  

"""
    Rota para deletar um usuario
"""
            
@auth_db.route('/deleteUser', methods=['DELETE'])
@auth_db.response(200, UserSchemaResponseSchema, description="User deleted successfully")
@auth_db.response(400, errorInvalidRequestDataSchema, description="Validation error")
@auth_db.response(401, errorTokenNotFoundSchema, description="Token not found")
@auth_db.response(404, errorUserNotFoundSchema, description="User not found")
def delete_user():
    session = Session()
    try:
        token = request.cookies.get('token')

        if not token:
            return (jsonify({"message": "Token not found."}), 403)
        
        payload = Token.decode_token(token)
        if "message" in payload:
            return (jsonify(payload.get("message")), 401)
        
        user_id = payload["user_id"]
        print(user_id)
        
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            return (jsonify({"message": "User not found."}), 404)
        
        session.delete(user)
        
        response = make_response(jsonify({"message": "User deleted successfully."}))     
        response.delete_cookie("token", httponly=True, samesite='None', secure=True)
        
        session.commit()
        return response
    except ValidationError as err:
        return (jsonify({"message": "Validation error", "errors": err.messages}), 400)
    finally:
        if session:
            session.close()
            
"""
    Rota para atualizar a senha
"""
            
@auth_db.route('/updatePassword', methods=['PUT'])
@auth_db.arguments(UserUpdatePasswordSchema)
@auth_db.response(200,  responseUserUpdatePasswordSchema, description="Password updated successfully")
@auth_db.response(400, errorInvalidRequestDataSchema, description="Validation error")
@auth_db.response(404, errorUserNotFoundSchema, description="User not found")
def update_password(data):
    session = Session()

    if(data['email'].strip() == "" or data['userName'].strip() == "" or data['newPassword'].strip() == ""):
        return jsonify({"message": "Invalid request data"}), 400

    try:
        user = session.query(User).filter((User.email == data['email']) & (User.userName == data['userName'])).first()
        if user:
            user.set_password(data['newPassword'])
            session.commit()
            return jsonify({"message": "Password updated successfully."}), 200
        else:

            return jsonify({"message": "User not found."}), 404
    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400
    finally:
        if session:
            session.close()


"""
    Rota para delogar
"""

@auth_db.route("/logout", methods=["POST"])
def logout():
    try:
        response = make_response(jsonify({"message": "Logout successful."}))
        response.delete_cookie("token", httponly=True, samesite='None', secure=True)
        return response
    except Exception :
        return jsonify({"message": "Logout failed."}), 500
       
# Register blueprints
api.register_blueprint(auth_db)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)


