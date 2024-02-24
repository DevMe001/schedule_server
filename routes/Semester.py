from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.Semester import Semester
from schemas.Semester import SemesterSchema
from datetime import datetime
from pydantic import UUID4
from typing import Optional, List, Union, Dict, Any
from auth.Oauth2 import get_current_user
from schemas.User import UserSchema
from models.User import User
router = APIRouter(prefix="/semesters", tags=["Semester"])


@router.get("/get", response_model=Dict[str, Union[str, List[Dict[str, Any]]]])
# for querying all the data from Courses
async def index(page: Optional[int] = 1, limit: Optional[int] = 10, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    offset = (page - 1) * limit
    # to query the entire created table from Courses db
    semesters = db.query(Semester).filter(Semester.deleted_at==None).offset(offset).limit(limit).all()
    data =[]
    if semesters:
        for semester in semesters:
            data.append({
                "id": semester.id,
                "name": semester.name,
                "order": semester.order,
                "created_at": semester.created_at,
                "created_by": semester.created_by,
                "updated_at": semester.updated_at,
                "updated_by": semester.updated_by
            })
    return{
        "message": "All semesters fetched successfully",
        "data": data
    }
@router.get("/getsemester")
# for querying all the data from Courses
async def index(db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    # to query the entire created table from Courses db
    semesters = db.query(Semester).filter(Semester.deleted_at == None).all()
    data = []
    if semesters:
        for semester in semesters:
            data.append({
                "id": semester.id,
                "name": semester.name,
                "order": semester.order,
                "created_at": semester.created_at,
                "created_by": semester.created_by,
                "updated_at": semester.updated_at,
                "updated_by": semester.updated_by
            })
    return {
        "message": "All semesters fetched successfully",
        "data": data
    }


@router.post("/post")
# para mag request ng post sa db thru api
async def store(request: SemesterSchema, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    semester = db.query(Semester).filter(Semester.name == request.name).all()

    if semester:
        raise HTTPException(status_code=400, detail=f"{request.name} already exists!")

    try:
        semester = Semester(
            name=request.name,
            order=request.order,
            created_at=datetime.now(),
            created_by=userid
        )
        db.add(semester)
        db.commit()
        return {
            "message": "Succesfully Added!",
            "data": {
                "name": semester.name,
                "order": semester.order,
                "created_at": semester.created_at,
                "created_by": semester.created_by
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{id}")
# For ensuring the id when accessed
async def show(id: UUID4, db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    semester = db.query(Semester).filter(Semester.id == id, Semester.deleted_at == None).first()

    if semester:
        return {
            "message": f"{semester.name} information fetched successfully !",
            "data": {
                "name": semester.name,
                "order": semester.order,
                "created_at": semester.created_at,
                "created_by": semester.created_by,
                "updated_at": semester.updated_at,
                "updated_by": semester.updated_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"Semester does not exists!")


@router.put("/{id}")
async def update(id: UUID4, request: SemesterSchema, db: Session = Depends(get_db),current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    semester = db.query(Semester).filter(Semester.id == id, Semester.deleted_at == None).first()

    if semester:
        semester.name = request.name
        semester.order = request.order
        semester.updated_at = datetime.now()
        semester.updated_by = userid
        db.commit()

        return {
            "message": f"The following information for {semester.name} has been updated successfully",
            "data": {
                "name": semester.name,
                "order": semester.order,
                "created_at": semester.created_at,
                "created_by": semester.created_by,
                "updated_at": semester.updated_at,
                "updated_by": semester.updated_by
            }
        }
    else:
         raise HTTPException(status_code=404, detail=f"Semester does not Exists!")


@router.delete("/{id}")
async def delete(id: UUID4, db: Session= Depends(get_db),current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    semester = db.query(Semester).filter(Semester.id == id, Semester.deleted_at == None).first()

    if semester:
            semester.deleted_at = datetime.now()
            semester.deleted_by = userid
            db.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Semester does not Exists!")