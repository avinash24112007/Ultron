import uuid
from datetime import datetime
from sqlalchemy import String, Text, Boolean, Integer, Numeric, DateTime, ForeignKey, text
from sqlalchemy .dialects.postgresql import  array 
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Users(Base):
    __tablename__ = "Users"
    User_ID : Mapped[int]= mapped_column(Integer,autoincrement=True, primary_key = True)
    user_name : Mapped[str] = mapped_column(String(50), nullable = False)
    email: Mapped[str] = mapped_column(String(100), nullable = False)
    password: Mapped[str] = mapped_column(String(20), nullable = False)
    Role:Mapped[str] = mapped_column(String(20), nullable = False)


class Chat(Base):
    __tablename__ = "Chats"
    Chat_ID : Mapped[str] = mapped_column(Integer,autoincrement = True, primary_key = True)
    Chat_name : Mapped[str] = mapped_column(String(50), nullable = False)
    User_Id : Mapped[int] = mapped_column(Integer(50), ForeignKey("Users.User_ID"), nullable = False)
    Human_message : Mapped[str] = mapped_column(String(1000), nullable = False)
    AI_message : Mapped[str] = mapped_column(String(1000))
    Upload_Doc : Mapped[str] = mapped_column(String(100))
    
class Enclaves(Base):
    __tablename__ = "Enclaves"

    Enclave_ID :Mapped[int] =  mapped_column(Integer,autoincrement = True, primary_key = True)
    Enclave_name:Mapped[str] = mapped_column(String(50), nullable = False)
    Type:Mapped[str] = mapped_column(String(50), nullable = False)
    date: Mapped[datetime] = mapped_column(DateTime(timezone = True), nullable = False)

class Assets(Base):

    __tablename__  = "Assets"
    
    Asset_ID :Mapped[int] =  mapped_column(Integer,autoincrement = True, primary_key = True)
    Asset_name:Mapped[str] = mapped_column(String(50), nullable = False)
    Size:Mapped[int] = mapped_column(Integer, nullable = False)
    date:Mapped[datetime] = mapped_column(DateTime(timezone = True),nullable = False)
    Status:Mapped[str] = mapped_column(String(50), nullable = False)
    file_type : Mapped[str] = mapped_column(String(10))
    file_path: Mapped[str] = mapped_column(String(100))

class Reports(Base):
    __tablename__ = "reports"

    Report_ID :Mapped[int] =  mapped_column(Integer,autoincrement = True, primary_key = True)
    Chat_ID :Mapped[int] =  mapped_column(Integer(50),ForeignKey("Chat.Chat_ID"), nullable = False)
    Report_name:Mapped[str] = mapped_column(String(50), nullable = False)
    output_file_path :Mapped[str] = mapped_column(String(100))
    date:Mapped[datetime] = mapped_column(DateTime.now(timezone.utc),nullable = False)




