from fastapi import APIRouter
from pydantic import BaseModel, Field
from fastapi import HTTPException
from datetime import datetime, date 

router = APIRouter()

# Exercício 2
# @app.get('/')
# def read_root():
#     return {"message": "Hello, FastAPI!"}

# Exercício 3
@router.get('/')
def read_root():
    return {"message": "Hello, FastAPI!"}

@router.get('/status')
def get_status():
    return {"status": "O servidor está funcionando"}


# Exercício 5
class UserResponse(BaseModel):
    username: str
    message: str

@router.get('/user/{username}', response_model=UserResponse)
def greet_user(username: str):
    return {"username": username, "message": f"Hello, {username}!"}

# Exercício 6
users_db = {
    "Patricia": "Olá, Patricia!",
    "Mateo": "Olá, Mateo!"
}

@router.get('/user/{username}', response_model=UserResponse)
def greet_user(username: str):
    if username not in users_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return {"username": username, "message": users_db[username]}


# Exercício 7
class UserCreateRequest(BaseModel):
    username: str
    age: int

@router.post('/create-user')
def create_user(user: UserCreateRequest):
    # Retorna os dados recebidos no corpo da requisição
    return {"username": user.username, "age": user.age}


# Exercício 8
class UserCreateRequest(BaseModel):
    username: str = Field(..., min_length=3, description="Nome de usuário deve ser uma string")
    age: int = Field(..., gt=0, description="Idade deve ser um número inteiro positivo")

@router.post('/create-user')
def create_user(user: UserCreateRequest):
    return {"username": user.username, "age": user.age}

# Exercício 9
users_db_v2 = {
    1: {"name": "Item 1", "description": "Patricia"},
    2: {"name": "Item 2", "description": "Mateo"},
    3: {"name": "Item 3", "description": "Fernanda"}
}

@router.get("/item/{item_id}")
def get_item(item_id: int):
    
    return users_db_v2[item_id]

@router.delete("/item/{item_id}")
def delete_item(item_id: int):
    del users_db_v2[item_id]
    
    return {"message": f"Item {item_id} deletado com sucesso"}


# Exercício 10
@router.get("/item/{item_id}")
def get_item(item_id: int):
    if item_id not in users_db_v2:
        raise HTTPException(status_code=400, detail="Item não existe")
    
    return users_db_v2[item_id]

@router.delete("/item/{item_id}")
def delete_item(item_id: int):
    if item_id not in users_db_v2:
        raise HTTPException(status_code=400, detail="Item não existe")
    
    del users_db_v2[item_id]
    
    return {"message": f"Item {item_id} deletado com sucesso"}


# Exercício 11
class BirthdayRequest(BaseModel):
    name: str = Field(..., min_length=1, description="Nome da pessoa")
    birthday: date = Field(..., description="Data de aniversário no formato YYYY-MM-DD")


def calculate_days_until_next_birthday(birthday: date) -> int:
    today = date.today()
    current_year_birthday = birthday.replace(year=today.year)

    if current_year_birthday < today:
        next_birthday = current_year_birthday.replace(year=today.year + 1)
    else:
        next_birthday = current_year_birthday

    return (next_birthday - today).days


@router.post('/birthday')
def birthday_calculator(request: BirthdayRequest):
    days_until_birthday = calculate_days_until_next_birthday(request.birthday)
    return {
        "message": f"Olá, {request.name}! Faltam {days_until_birthday} dias até seu próximo aniversário."
    }
