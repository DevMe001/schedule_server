from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.YearLevel import YearLevel
from schemas.YearLevel import YearLevelSchema
from datetime import datetime
from pydantic import UUID4
from auth.Oauth2 import get_current_user
from schemas.User import UserSchema
from models.User import User
from typing import Optional, List, Union, Dict, Any

router = APIRouter(prefix="/yearlevels", tags=["YearLevel"])


@router.get("/get", response_model=Dict[str, Union[str, List[Dict[str, Any]]]])
# for querying all the data from Courses
async def index(page: Optional[int] = 1, limit: Optional[int] = 10, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    offset = (page - 1) * limit
    yearlevels = db.query(YearLevel).filter(YearLevel.deleted_at==None).offset(offset).limit(limit).all()
    data =[]
    if yearlevels:
        for yearlevel in yearlevels:
            data.append({
                "id": yearlevel.id,
                "name": yearlevel.name,
                "order": yearlevel.order,
                "created_at": yearlevel.created_at,
                "created_by": yearlevel.created_by,
                "updated_at": yearlevel.updated_at,
                "updated_by": yearlevel.updated_by
            })
    return{
        "message": "All year levels fetched successfully",
        "data": data
    }

@router.get("/getyearlevels")
# for querying all the data from Courses
async def index(db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    yearlevels = db.query(YearLevel).filter(YearLevel.deleted_at==None).all()
    if yearlevels:
        data = []
        for yearlevel in yearlevels:
            data.append({
                "id": yearlevel.id,
                "name": yearlevel.name,
                "order": yearlevel.order,
                "created_at": yearlevel.created_at,
                "created_by": yearlevel.created_by,
                "updated_at": yearlevel.updated_at,
                "updated_by": yearlevel.updated_by
            })
    return{
        "message": "All year levels fetched successfully",
        "data": data
    }

@router.post("/post")
# para mag request ng post sa db thru api
async def store(request: YearLevelSchema, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    yearlevel = db.query(YearLevel).filter(YearLevel.name == request.name).all()

    if yearlevel:
        raise HTTPException(status_code=400, detail=f"Year level {request.name} already exists!")

    try:
        yearlevel = YearLevel(
            name=request.name,
            order=request.order,
            created_at=datetime.now(),
            created_by=userid
        )
        db.add(yearlevel)
        db.commit()
        return {
            "message": "Succesfully Added!",
            "data": {
                "name": yearlevel.name,
                "order": yearlevel.order,
                "created_at": yearlevel.created_at,
                "created_by": yearlevel.created_by
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{id}")
# For ensuring the id when accessed
async def show(id: UUID4, db: Session = Depends(get_db),current_user: UserSchema = Depends(get_current_user)):
    yearlevel = db.query(YearLevel).filter(YearLevel.id == id, YearLevel.deleted_at == None).first()

    if yearlevel:
        return {
            "message": f"{yearlevel.name} level fetched successfully !",
            "data": {
                "name": yearlevel.name,
                "order": yearlevel.order,
                "created_at": yearlevel.created_at,
                "created_by": yearlevel.created_by,
                "updated_at": yearlevel.updated_at,
                "updated_by": yearlevel.updated_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"Year level does not exists!")


@router.put("/{id}")
async def update(id: UUID4, request: YearLevelSchema, db: Session = Depends(get_db),current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    yearlevel = db.query(YearLevel).filter(YearLevel.id == id, YearLevel.deleted_at == None).first()

    if yearlevel:
        yearlevel.name = request.name
        yearlevel.order = request.order
        yearlevel.updated_at = datetime.now()
        yearlevel.updated_by = userid
        db.commit()

        return {
            "message": f"Year level {yearlevel.name} has been updated successfully",
            "data": {
                "name": yearlevel.name,
                "order": yearlevel.order,
                "created_at": yearlevel.created_at,
                "created_by": yearlevel.created_by,
                "updated_at": yearlevel.updated_at,
                "updated_by": yearlevel.updated_by
            }
        }
    else:
         raise HTTPException(status_code=404, detail=f"Year level does not exists!")


@router.delete("/{id}")
async def delete(id: UUID4, db: Session= Depends(get_db),current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    yearlevel = db.query(YearLevel).filter(YearLevel.id == id, YearLevel.deleted_at == None).first()

    if yearlevel:
            yearlevel.deleted_at = datetime.now()
            yearlevel.deleted_by = userid
            db.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Year level does not Exists!")
