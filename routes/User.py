from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.User import User
from schemas.User import UserSchema
from schemas.UpdateUser import UpdateUserSchema
from datetime import datetime
from pydantic import UUID4
from hash.Hashing import Hash
from auth.Oauth2 import get_current_user
#from passlib.context import CryptContext

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
# for querying all the data from Courses
async def index(db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    # to query the entire created table from Courses db
    users = db.query(User).filter(User.deleted_at == None).all()
    data = []
    if users:
        for user in users:
            data.append({
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "usertype": user.usertype,
                "updated_at": user.updated_at
            })
    return {
        "message": "user fetched successfully",
        "data": data
    }


@router.post("/")
# para mag request ng post sa db thru api
async def store(request: UserSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).all()

    if user:
        raise HTTPException(status_code=400, detail="email already exists!")

    try:
        user = User(
            email=request.email,
            password=Hash.bcrypt(request.password),
            first_name=request.first_name,
            last_name=request.last_name,
            usertype=request.usertype,
            created_at=datetime.now()
        )
        db.add(user)
        db.commit()
        return {
            "message": "Succesfully Added!",
            "data": {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "usertype": user.usertype,
                "created_at": user.created_at
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{id}")
# For ensuring the id when accessed
async def show(id: UUID4, db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.id == id, User.deleted_at == None).first()

    if user:
        return {
            "message": "User fetched successfully",
            "data": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "usertype": user.usertype,
                "updated_at": user.updated_at,
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"User does not exists!")


@router.put("/{id}")
async def update(id: UUID4, request: UpdateUserSchema, db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.id == id, User.deleted_at == None).first()

    if user:
        user.first_name = request.first_name
        user.last_name = request.last_name
        user.usertype = request.usertype
        user.updated_at = datetime.now()
        db.commit()

        return {
            "message": "Account updated successfully",
            "data": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "updated_at": user.updated_at
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"User does not exists!")



@router.delete("/{id}")
async def delete(id: UUID4, db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    course = db.query(User).filter(User.id == id, User.deleted_at == None).first()

    if course:
        User.deleted_at = datetime.now()
        db.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Course does not exists!")
