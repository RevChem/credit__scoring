from sqlalchemy import text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, str_uniq, int_pk
from app.diagnosiss.models import Diagnosis
from app.users.sql_enums import GenderEnum


class User(Base):
    id: Mapped[int_pk]
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str_uniq]
    last_name: Mapped[str | None]
    age: Mapped[int | None]
    gender: Mapped[GenderEnum]
    email: Mapped[str_uniq]
    password: Mapped[str]

    extend_existing = True

    diagnosis: Mapped[list["Diagnosis"]] = relationship(
        "Diagnosis", back_populates="user")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, first_name={self.first_name!r}, last_name={self.last_name!r})"

    def __repr__(self):
        return str(self)


    def to_dict(self):
        return {
            "id": self.id,
            "phone_number": self.phone_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "gender": self.gender,
            "email": self.email,
            "password": self.password  
        }