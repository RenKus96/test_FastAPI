from fastapi import FastAPI
from typing import Optional, List, Dict
from pydantic import BaseModel


class User(BaseModel):
    id: Optional[int]
    name: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


# users = {
#     1: {
#         "name": "Vladimir",
#         "email": "test@gmail.com",
#         "full_name": "Karpov Vladimir Petrovih",
#         "is_active": "True",
#         "is_superuser": "False"
#     },
#     2: {
#         "name": "Vlad",
#         "email": "test2@gmail.com",
#         "full_name": "Kapov Vlad Petrovih",
#         "is_active": "True",
#         "is_superuser": "False"
#     },
#     3: {
#         "name": "Valera",
#         "email": "test3@gmail.com",
#         "full_name": "Kapov Valera Petrovih",
#         "is_active": "True",
#         "is_superuser": "False"
#     }
# }

users = [
    {
        "id": 1,
        "name": "Vladimir",
        "email": "test@gmail.com",
        "full_name": "Karpov Vladimir Petrovih",
        "is_active": "True",
        "is_superuser": "False"
    },
    {
        "id": 2,
        "name": "Vlad",
        "email": "test2@gmail.com",
        "full_name": "Kapov Vlad Petrovih",
        "is_active": "True",
        "is_superuser": "False"
    },
    {
        "id": 3,
        "name": "Valera",
        "email": "test3@gmail.com",
        "full_name": "Kapov Valera Petrovih",
        "is_active": "True",
        "is_superuser": "False"
    }
]

def get_user_from_list(user_id):
    for user in users:
        if user['id'] == user_id:
            return user

app = FastAPI()

@app.get('/')
def main():
    return {"hello":"world"}

@app.get('/user/{user_id}', response_model=User)
def get_user(user_id: int):
    return get_user_from_list(user_id)

@app.get('/users/', response_model=List[User])
def get_users():
    return users

# @app.get('/users/', response_model=List[User])
# def get_users():
#     users_out = [user for (key, user) in users.items()]
#     return users_out

# @app.get('/users/', response_model=Dict)
# def get_users():
#     return users
