# 1. Нужно поднять fastapi . Эндпоинты:
# /create-user
# /update-password
# /delete-user
# /get-user-list
#
# Сохранять пользователей пока в переменную в скрипте. Базу потом подключим.
# Запросы отправлять через постман в виде json

from fastapi import FastAPI
from typing import Optional, List, Dict
from pydantic import BaseModel
import json

class User(BaseModel):
    # id: Optional[int]
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

# users = [
#     {
#         "id": 1,
#         "name": "Vladimir",
#         "email": "test@gmail.com",
#         "full_name": "Karpov Vladimir Petrovih",
#         "is_active": "True",
#         "is_superuser": "False"
#     },
#     {
#         "id": 2,
#         "name": "Vlad",
#         "email": "test2@gmail.com",
#         "full_name": "Kapov Vlad Petrovih",
#         "is_active": "True",
#         "is_superuser": "False"
#     },
#     {
#         "id": 3,
#         "name": "Valera",
#         "email": "test3@gmail.com",
#         "full_name": "Kapov Valera Petrovih",
#         "is_active": "True",
#         "is_superuser": "False"
#     }
# ]

def save_users_json():
    with open('users.json', 'w') as json_file:
        json.dump(users, json_file)

# def get_user_from_list(user_id):
#     for user in users:
#         if user['id'] == user_id:
#             return user


with open('users.json') as json_file:
    users = json.load(json_file)

app = FastAPI()


@app.on_event("shutdown")
def shutdown():
    save_users_json()

@app.get('/')
def main():
    return {"hello":"world"}


# @app.get('/user/{user_id}', response_model=User)
# def get_user(user_id: int):
#     return get_user_from_list(user_id)


@app.get('/user/{user_id}', response_model=User)
def get_user(user_id: int):
    return users[str(user_id)]


# @app.get('/get-user-list/', response_model=List[User])
# def get_users():
#     return users


@app.get('/get-user-list/', response_model=List[User])
def get_users():
    users_out = [user for (key, user) in users.items()]
    return users_out


# @app.get('/get-user-list/', response_model=Dict)
# def get_users():
#     return users

@app.post('/create-user/', response_model=User)
def create_user(user: User):
    user_dict = user.dict()
    users[str(len(users)+1)] = user_dict
    save_users_json()
    return user

@app.delete('/delete-user/{user_id}')
def delete_user(user_id: int):
    if users.pop(str(user_id), None):
        save_users_json()
        return {'msg': f'User_id {user_id} has been deleted succesfully'}
    else:
        return {'msg': f'User_id {user_id} not found'}

