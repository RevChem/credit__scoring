from app.users.sql_enums import GenderEnum

class RBUser:
    def __init__(
        self,
        id: int | None = None,
        first_name: str | None = None,
        phone_number: str | None = None,
        last_name: str | None = None,
        age: int | None = None,
        gender: GenderEnum | None = None,
        email: str | None = None,
        password: str | None = None,
    ):
        self.id = id
        self.first_name = first_name
        self.phone_number = phone_number
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.email = email
        self.password = password

    def to_dict(self) -> dict:
        return {
            key: value for key, value in {
                "id": self.id,
                "first_name": self.first_name,
                "phone_number": self.phone_number,
                "last_name": self.last_name,
                "age": self.age,
                "gender": self.gender,
                "email": self.email,
                "password": self.password
            }.items() if value is not None
        }