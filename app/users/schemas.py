import re
from typing import Optional
from app.users.sql_enums import GenderEnum
from pydantic import BaseModel, EmailStr, Field, field_validator


class SUser(BaseModel):
    email: Optional[EmailStr] = Field(None, description="Электронная почта")
    gender: Optional[GenderEnum]
    password: Optional[str] = Field(None, min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    phone_number: Optional[str] = Field(None, description="Номер телефона в международном формате, начинающийся с '+'")
    first_name: Optional[str] = Field(None, min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    last_name: Optional[str] = Field(None, min_length=3, max_length=50, description="Фамилия, от 3 до 50 символов")

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        if not re.match(r'^\+\d{5,15}$', values):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 5 до 15 цифр')
        return values


