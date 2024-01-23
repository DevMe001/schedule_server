from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.User import User
from config.database import get_db
from hash.Hashing import Hash
from auth.token import create_access_token
from schemas.Login import LoginSchema
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/login", tags=["Login"])


@router.post('/sign-in')
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials!")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Password!")

    # Fetch usertype from the user object
    usertype = user.usertype

    # Include usertype in the token payload
    access_token = create_access_token(data={"sub": user.email, "usertype": usertype})
    return {"access_token": access_token, "token_type": "bearer"}