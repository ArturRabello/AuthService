
import datetime
from typing import List
from marshmallow import Schema, fields

"""
    Esquema de usuário
    apresenta esquemas de entrada e saida,
"""

class UserRegisterSchema(Schema):
    userName = fields.Str(load_default="admin")
    email = fields.Str(load_default="admin@yahoo.com")
    password = fields.Str(load_default="admin")
    passwordConfirm = fields.Str(load_default="admin")

class UserLoginSchema(Schema):
    email = fields.Str(load_default="admin@yahoo.com")
    password= fields.Str(load_default="admin")


class UserSchemaResponseSchema(Schema):
    id = fields.Int(load_default=1)
    userName = fields.Str(load_default="admin")
    email = fields.Str(load_default="admin@yahoo.com")
    
class UserListSchema(Schema):
    users = fields.List(fields.Nested(UserSchemaResponseSchema))
    
def returnUser(user):
    return {
        "id": user.id, 
        "userName": user.userName,
        "email": user.email
        }

def returnUserList( users):
    result = []
    for user in users:
        result.append(returnUser(user))
    return{"users": result}

class UserSearchSchema(Schema):
    id = fields.Int(load_default=1)
    userName = fields.Str(load_default="admin")
    email = fields.Str(load_default="admin@yahoo.com")

    
class responseUserSchema(Schema):
    errors = fields.Dict(load_default={"message": "User registered successfully"})
    
class errorInvalidRequestDataSchema(Schema):
    errors = fields.Dict(load_default={"message": "Invalid request data"})
    
class errorDatabaseErrorSchema(Schema):
    errors = fields.Dict(load_default={"message": "Database error"})
    
class errorEmailAlreadyExistsSchema(Schema):
      errors = fields.Dict(load_default={"message": "Email already exists"})

class errorPasswordNotMatchSchema(Schema):
    errors = fields.Dict(load_default={"message": "Passwords do not match"})
    
class errorLoginSchema(Schema):
    errors = fields.Dict(load_default={"message": "Invalid password"})
    
class errorUserNotFoundSchema(Schema):
    errors = fields.Dict(load_default={"message": "User not found"})

class erroInvalidPasswordSchema(Schema):
    errors = fields.Dict(load_default={"message": "Invalid token"})
    
class UserUpdatePasswordSchema(Schema):
    userName = fields.Str(load_default="admin")
    email = fields.Str(load_default="admin@yahoo.com")
    newPassword = fields.Str(load_default="admin")
    
class responseUserUpdatePasswordSchema(Schema):
    errors = fields.Dict(load_default={"message": "Password updated successfully"})

class errorTokenNotFoundSchema(Schema):
    errors = fields.Dict(load_default={"message": "Token not found"})

class TokenSchema(Schema):
    token = fields.String(required=False)


class errorEmptyfilds(Schema):
    errors = fields.Dict(load_default={"message": "Emptyfilds"})

class errorEmptyNamefilds(Schema):
    errors = fields.Dict(load_default={"message": "Empty name filds"})

class errorEmptyEmailfilds(Schema):
    errors = fields.Dict(load_default={"message": "Empty email filds"})

class errorEmptyPasswordfilds(Schema):
    errors = fields.Dict(load_default={"message": "Empty password filds"})

class errorEmptyPasswordConfirmfilds(Schema):
    errors = fields.Dict(load_default={"message": "Empty passwordConfirm filds"})

    


    
    


    
    