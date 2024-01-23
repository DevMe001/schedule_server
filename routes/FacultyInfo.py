from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.FacultyInfo import FacultyInfo
from schemas.FacultyInfo import FacultyInfoSchema
from datetime import datetime
from pydantic import UUID4
from auth.Oauth2 import get_current_user
from schemas.User import UserSchema
from models.User import User
from typing import Optional, List, Union, Dict, Any

router = APIRouter(prefix="/faculties", tags=["Faculties"])


@router.get("/get", response_model=Dict[str, Union[str, List[Dict[str, Any]]]])
async def index(page: Optional[int] = 1, limit: Optional[int] = 10, db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    # Calculate the offset based on page and limit
    offset = (page - 1) * limit
    # Query the database with pagination
    faculties = db.query(FacultyInfo).filter(FacultyInfo.deleted_at == None).offset(offset).limit(limit).all()
    data = []
    if faculties:
        for faculty in faculties:
            data.append({
                "id": faculty.id,
                "name": faculty.name,
                "status": faculty.status,
                "allowed_units": faculty.allowed_units,
                "preferred_schedule": faculty.preferred_schedule,
                "created_at": faculty.created_at,
                "created_by": faculty.created_by,
                "updated_at": faculty.updated_at,
                "updated_by": faculty.updated_by
            })
    return {
        "message": "faculties fetched successfully",
        "data": data
    }


@router.get("/getfaculties")
# for querying all the data from Courses
async def index(db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    # to query the entire created table from Courses db
    faculties = db.query(FacultyInfo).filter(FacultyInfo.deleted_at == None).all()
    data = []
    if faculties:
        for faculty in faculties:
            data.append({
                "id": faculty.id,
                "name": faculty.name,
                "status": faculty.status,
                "allowed_units": faculty.allowed_units,
                "preferred_schedule": faculty.preferred_schedule,
                "created_at": faculty.created_at,
                "created_by": faculty.created_by,
                "updated_at": faculty.updated_at,
                "updated_by": faculty.updated_by
            })
    return {
        "message": "Course fetched successfully",
        "data": data
    }


@router.post("/post")
async def store(request: FacultyInfoSchema, db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    faculty = db.query(FacultyInfo).filter(FacultyInfo.name == request.name).all()

    if faculty:
        raise HTTPException(status_code=400, detail=f"Faculty {request.name} already exists!")

    try:
        faculty = FacultyInfo(
            name=request.name,
            status=request.status,
            allowed_units=request.allowed_units,
            preferred_schedule=request.preferred_schedule,
            created_at=datetime.now(),
            created_by=userid
        )
        db.add(faculty)
        db.commit()
        return {
            "message": "Succesfully Added!",
            "data": {
                "name": faculty.name,
                "status": faculty.status,
                "allowed_units": faculty.allowed_units,
                "preferred_schedule": faculty.preferred_schedule,
                "created_at": faculty.created_at,
                "created_by": faculty.created_by
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{id}")
# For ensuring the id when accessed
async def show(id: UUID4, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    faculty = db.query(FacultyInfo).filter(FacultyInfo.id == id, FacultyInfo.deleted_at == None).first()

    if faculty:
        return {
            "message": f"Faculty fetched successfully {faculty.name}",
            "data": {
                "name": faculty.name,
                "status": faculty.status,
                "allowed_units": faculty.allowed_units,
                "preferred_schedule": faculty.preferred_schedule,
                "created_at": faculty.created_at,
                "created_by": faculty.created_by,
                "updated_at": faculty.updated_at,
                "updated_by": faculty.updated_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"faculty does not exists!")


@router.put("/{id}")
async def update(id: UUID4, request: FacultyInfoSchema, db: Session = Depends(get_db),
                 current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    faculty = db.query(FacultyInfo).filter(FacultyInfo.id == id, FacultyInfo.deleted_at == None).first()

    if faculty:
        faculty.name = request.name
        faculty.status = request.status
        faculty.allowed_units = request.allowed_units
        faculty.preferred_schedule = request.preferred_schedule
        faculty.updated_at = datetime.now()
        faculty.updated_by = userid
        db.commit()

        return {
            "message": f"faculty {faculty.name} updated successfully",
            "data": {
                "name": faculty.name,
                "status": faculty.status,
                "allowed_units": faculty.allowed_units,
                "preferred_schedule": faculty.preferred_schedule,
                "created_at": faculty.created_at,
                "created_by": faculty.created_by,
                "updated_at": faculty.updated_at,
                "updated_by": faculty.updated_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"Course does not exists!")


@router.delete("/{id}")
async def delete(id: UUID4, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    faculty = db.query(FacultyInfo).filter(FacultyInfo.id == id, FacultyInfo.deleted_at == None).first()

    if faculty:
        faculty.deleted_at = datetime.now()
        faculty.deleted_by = userid
        db.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Course does not exists!")
