from fastapi import Form
from pydantic import BaseModel

class UserDelete(BaseModel):
    password: str

    @classmethod
    def delete(cls, password: str = Form(...)):
        return cls(password=password)