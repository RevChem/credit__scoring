from fastapi import APIRouter, Depends
from app.users.dao import UserDAO
from app.users.schemas import SUser
from typing import Optional
from app.users.rb import RBUser


router = APIRouter(prefix = '/users', tags = ['Работа с пользователями'])

@router.get("/{id}", summary="Получить пользователя по ID")
async def find_one_or_none_by_id(request_body: RBUser = Depends()) -> Optional[SUser]:
    return await UserDAO.find_one_or_none_by_id(**request_body.to_dict())


@router.get("/", summary="Получить всех пользователей")
async def find_all() -> list[SUser]:
    return await UserDAO.find_all()


@router.post("/add/")
async def add_user(user: SUser) -> dict:
    user = await UserDAO.add(**user.dict())
    if user:
        return {"message": "Пользователь успешно добавлен!", "user": user}
    else:
        return {"message": "Ошибка при добавлении пользователя!"}


@router.delete("/dell/{id}")
async def delete(id: int) -> dict:
    check = await UserDAO.delete(id=id)
    if check:
        return {"message": f"Студент с ID {id} удален!"}
    else:
        return {"message": "Ошибка при удалении студента!"}