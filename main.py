# 1. Нужно поднять fastapi . Эндпоинты:
# /create-user
# /update-password
# /delete-user
# /get-user-list
#
# Сохранять пользователей пока в переменную в скрипте. Базу потом подключим.
# Запросы отправлять через постман в виде json

from fastapi import FastAPI
from typing import Optional, List, Dict, Union
from pydantic import BaseModel
import json

class User(BaseModel):
    # id: Optional[int]
    name: str
    password: str
    email: str
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

class User_no_pwd(BaseModel):
    # id: Optional[int]
    name: str
    email: str
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

class Password(BaseModel):
    id: int
    password: str

class User_id(BaseModel):
    id: int

class User_update(BaseModel):
    id: int
    user: User

users = {
    1: {
        "name": "Vladimir",
        "password": "pass1",
        "email": "test@gmail.com",
        "full_name": "Karpov Vladimir Petrovih",
        "is_active": "True",
        "is_superuser": "False"
    },
    2: {
        "name": "Vlad",
        "password": "pass2",
        "email": "test2@gmail.com",
        "full_name": "Kapov Vlad Petrovih",
        "is_active": "True",
        "is_superuser": "False"
    },
    3: {
        "name": "Valera",
        "password": "pass3",
        "email": "test3@gmail.com",
        "full_name": "Kapov Valera Petrovih",
        "is_active": "True",
        "is_superuser": "False"
    }
}

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

# def save_users_json():
#     with open('users.json', 'w') as json_file:
#         json.dump(users, json_file)

# def get_user_from_list(user_id):
#     for user in users:
#         if user['id'] == user_id:
#             return user
#     return None
#
# with open('users.json') as json_file:
#     users = json.load(json_file)

app = FastAPI()


# @app.on_event("shutdown")
# def shutdown():
#     save_users_json()

@app.get('/')
def main():
    return {"hello":"world"}


# @app.get('/user/{user_id}', response_model=User)
# def get_user(user_id: int):
#     return get_user_from_list(user_id)


# @app.get('/user/{user_id}', response_model=User)
# def get_user(user_id: int):
#     return users[user_id]

@app.get('/user/', response_model=User_no_pwd)
def get_user(param: User_id):
    user_id = param.dict()['id']
    if users.get(user_id):
        return users.get(user_id)


# Если users типа List
# @app.get('/get-user-list/', response_model=List[User])
# def get_users():
#     return users


# Если users типа Dict, но выводим List
# @app.get('/get-user-list/', response_model=List[User])
# def get_users():
#     users_out = [user for (id, user) in users.items()]
#     return users_out


# Если users типа Dict
@app.get('/get-user-list/', response_model=Dict[int, User_no_pwd])
def get_users():
    return users


@app.post('/create-user/', response_model=User_no_pwd)
def create_user(user: User):
    user_dict = user.dict()
    users[max(users)+1] = user_dict
    # save_users_json()
    return user_dict


@app.delete('/delete-user/', response_model=Dict)
def delete_user(param: User_id):
    user_id = param.dict()['id']
    user = users.pop(user_id, None)
    if user:
        # save_users_json()
        return {'msg': f'User {user["full_name"]} has been deleted succesfully'}
    else:
        return {'msg': f'User_id {user_id} not found'}


@app.patch('/update-password/', response_model=Dict)
def update_password(param: Password):
    pwd = param.dict()
    user = users.get(pwd['id'])
    if user:
        user['password'] = pwd['password']
        users[pwd['id']] = user
        return {'msg': f'Password for User_id {pwd["id"]} was change succesfully'}
    else:
        return {'msg': f'User_id {pwd["id"]} not found'}


@app.put('/update-user/', response_model=User_no_pwd)
def update_password(user_upd: User_update):
    user_id = user_upd.dict()['id']
    if users.get(user_id) :
        users[user_id] = user_upd.dict()['user']
        return users.get(user_id)
