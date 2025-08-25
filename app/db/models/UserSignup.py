from fastapi import Form
from app.db.models.UserLogin import UserLogin

class UserSignup(UserLogin):
    name: str
    surname: str

    @classmethod
    def signup(cls, username: str = Form(...), password: str = Form(...) , name: str = Form(...), surname: str = Form(...)):
        return cls(username=username, password=password, name=name, surname=surname)