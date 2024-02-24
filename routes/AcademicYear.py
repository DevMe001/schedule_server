from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.AcademicYear import AcademicYear
from schemas.AcademicYear import AcademicYearSchema
from datetime import datetime
from pydantic import UUID4
from auth.Oauth2 import get_current_user
from schemas.User import UserSchema
from models.User import User
from typing import Optional, List, Union, Dict, Any

router = APIRouter(prefix="/academicyears", tags=["Academic Year"])


@router.get("/get", response_model=Dict[str, Union[str, List[Dict[str, Any]]]])
# for querying all the data from Courses
async def index(page: Optional[int] = 1, limit: Optional[int] = 10, db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    offset = (page - 1) * limit
    acads = db.query(AcademicYear).filter(AcademicYear.deleted_at == None).offset(offset).limit(
        limit).all()
    data = []
    if acads:
        for acad in acads:
            data.append({
                "id": acad.id,
                "name": acad.name,
                "order": acad.order,
                "created_at": acad.created_at,
                "created_by": acad.created_by,
                "updated_at": acad.updated_at,
                "updated_by": acad.updated_by
            })
    return {
        "message": "All created academic years fetched successfully",
        "data": data
    }

@router.get("/getacadyr")
# for querying all the data from Courses
async def index(db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    acads = db.query(AcademicYear).filter(AcademicYear.deleted_at == None).all()
    data = []
    if acads:
        for acad in acads:
            data.append({
                "id": acad.id,
                "name": acad.name,
                "order": acad.order,
                "created_at": acad.created_at,
                "created_by": acad.created_by,
                "updated_at": acad.updated_at,
                "updated_by": acad.updated_by
            })
    return {
        "message": "All created acad year names fetched successfully",
        "data": data
    }



@router.post("/post")
# para mag request ng post sa db thru api
async def store(request: AcademicYearSchema, db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    acad = db.query(AcademicYear).filter(AcademicYear.name == request.name).all()

    if acad:
        raise HTTPException(status_code=400, detail=f"Year level {request.name} already exists!")

    try:
        acad = AcademicYear(
            name=request.name,
            order=request.order,
            created_at=datetime.now(),
            created_by=userid
        )
        db.add(acad)
        db.commit()
        return {
            "message": "Succesfully Added!",
            "data": {
                "name": acad.name,
                "order": acad.order,
                "created_at": acad.created_at,
                "created_by": acad.created_by
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{id}")
# For ensuring the id when accessed
async def show(id: UUID4, db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    acad = db.query(AcademicYear).filter(AcademicYear.id == id,
                                                     AcademicYear.deleted_at == None).first()

    if acad:
        return {
            "message": f"{acad.name} level fetched successfully !",
            "data": {
                "name": acad.name,
                "order": acad.order,
                "created_at": acad.created_at,
                "created_by": acad.created_by,
                "updated_at": acad.updated_at,
                "updated_by": acad.updated_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"Year level does not exists!")


@router.put("/{id}")
async def update(id: UUID4, request: AcademicYearSchema, db: Session = Depends(get_db),
                 current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    acad = db.query(AcademicYear).filter(AcademicYear.id == id,
                                                     AcademicYear.deleted_at == None).first()

    if acad:
        acad.name = request.name
        acad.order = request.order
        acad.updated_at = datetime.now()
        acad.updated_by = userid
        db.commit()

        return {
            "message": f"Year level {acad.name} has been updated successfully",
            "data": {
                "name": acad.name,
                "order": acad.order,
                "created_at": acad.created_at,
                "created_by": acad.created_by,
                "updated_at": acad.updated_at,
                "updated_by": acad.updated_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"Acadyr name does not exists!")


@router.delete("/{id}")
async def delete(id: UUID4, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    acad = db.query(AcademicYear).filter(AcademicYear.id == id,
                                                     AcademicYear.deleted_at == None).first()

    if acad:
        acad.deleted_at = datetime.now()
        acad.deleted_by = userid
        db.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Year level does not Exists!")
