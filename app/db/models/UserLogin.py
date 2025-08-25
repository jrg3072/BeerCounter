from fastapi import Form
from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str

    @classmethod
    def login(cls, username: str = Form(...), password: str = Form(...)):
        return cls(username=username, password=password)