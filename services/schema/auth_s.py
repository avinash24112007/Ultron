from pydantic import BaseModel
from typing import Optional

class pyd_login(BaseModel):
    email:str
    passcode:str


class pyd_register(BaseModel):
    UUser_ID :int
    user_name : str
    email:str
    passcode: str
    Role:str


class UserCreate(BaseModel):
    user_name: str
    email: str
    password: str
    Role: str

class ChatCreate(BaseModel):
    Chat_name: str
    User_Id: int
    Human_message: str
    AI_message: str | None = None
    Upload_Doc: str | None = None
    
