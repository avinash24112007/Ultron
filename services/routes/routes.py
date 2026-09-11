from model import Users, Chat,Enclaves, Assets,Reports
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from security import hash_password,verify_password
from sessionmaker import make_db_session
from auth_s import pyd_login, pyd_register, UserCreate, ChatCreate

routes = APIRouter(prefix = "/api/add")


@routes.post('/register')
def register(request: pyd_register, db: Session = Depends(make_db_session)):
    existing = db.query(Users).filter(Users.email == request.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    new_user = Users(
        user_name=request.user_name,
        email=request.email,
        passcode=hash_password(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "status": "success",
        "message": "User registered successfully!",
        "user_id": new_user.User_ID
    }


@routes.post('/login')
def login(request: pyd_login, db: Session = Depends(make_db_session)):
    instance = db.query(Users).filter(Users.email == request.email).first()

    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not verify_password(request.password, str(instance.passcode)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    return {
        "status": "success",
        "message": "Login successful!",
        "user_id": instance.User_ID,
        "role": instance.Role
    }

@routes.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(make_db_session)):
    db_user = Users(
        user_name=user.user_name,
        email=user.email,
        password=user.password,  # Note: Hash passwords in production
        Role=user.Role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created successfully", "user_id": db_user.User_ID}

@routes.post("/chats/", status_code=status.HTTP_201_CREATED)
def create_chat(chat: ChatCreate, db: Session = Depends(make_db_session)):
    # Verify user exists before attaching chat
    user_exists = db.query(Users).filter(Users.User_ID == chat.User_Id).first()
    if not user_exists:
        raise HTTPException(status_code=400, detail="User_Id does not exist")

    db_chat = Chat(
        Chat_name=chat.Chat_name,
        User_Id=chat.User_Id,
        Human_message=chat.Human_message,
        AI_message=chat.AI_message,
        Upload_Doc=chat.Upload_Doc
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return {"message": "Chat logged successfully", "chat_id": db_chat.Chat_ID}

@routes.get("/users/{user_id}/chats")
def get_user_chats(user_id: int, db: Session = Depends(make_db_session)):
    chats = db.query(Chat).filter(Chat.User_Id == user_id).all()
    return chats
