from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.Course import Course
from schemas.Course import CourseSchema
from datetime import datetime
from pydantic import UUID4
from auth.Oauth2 import get_current_user
from schemas.User import UserSchema
from models.User import User
from typing import Optional, List, Union, Dict, Any

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/get", response_model=Dict[str, Union[str, List[Dict[str, Any]]]])
async def index(page: Optional[int] = 1, limit: Optional[int] = 10, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    # Calculate the offset based on page and limit
    offset = (page - 1) * limit
    # Query the database with pagination
    courses = db.query(Course).filter(Course.deleted_at == None).offset(offset).limit(limit).all()
    data = []
    if courses:
        for course in courses:
            data.append({
                "id": course.id,
                "code": course.code,
                "name": course.name,
                "description": course.description,
                "created_at": course.created_at,
                "created_by": course.created_by,
                "updated_at": course.updated_at,
                "updated_by": course.updated_by
            })
    return {
        "message": "Course fetched successfully",
        "data": data
    }

@router.get("/getcourse")
# for querying all the data from Courses
async def index(db: Session = Depends(get_db)):
    # to query the entire created table from Courses db
    courses = db.query(Course).filter(Course.deleted_at == None).all()
    data = []
    if courses:
        for course in courses:
            data.append({
                "id": course.id,
                "code": course.code,
                "name": course.name,
                "description": course.description,
                "created_at": course.created_at,
                "created_by": course.created_by,
                "updated_at": course.updated_at,
                "updated_by": course.updated_by
            })
    return {
        "message": "Course fetched successfully",
        "data": data
    }

@router.post("/post")
async def store(request: CourseSchema, db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    course = db.query(Course).filter(Course.code == request.code).all()

    if course:
        raise HTTPException(status_code=400, detail=f"Course with code {request.code} already exists!")

    try:
        course = Course(
            code=request.code,
            name=request.name,
            description=request.description,
            created_at=datetime.now(),
            created_by=userid
        )
        db.add(course)
        db.commit()
        return {
            "message": "Succesfully Added!",
            "data": {
                "code": course.code,
                "name": course.name,
                "description": course.description,
                "created_at": course.created_at,
                "created_by": course.created_by
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{id}")
# For ensuring the id when accessed
async def show(id: UUID4, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == id, Course.deleted_at == None).first()

    if course:
        return {
            "message": f"Course fetched successfully with code {course.code}",
            "data": {
                "code": course.code,
                "name": course.name,
                "description": course.description,
                "created_at": course.created_at,
                "created_by": course.created_by,
                "updated_at": course.updated_at,
                "updated_by": course.updated_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"Course does not exists!")


@router.put("/{id}")
async def update(id: UUID4, request: CourseSchema, db: Session = Depends(get_db),current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    course = db.query(Course).filter(Course.id == id, Course.deleted_at == None).first()

    if course:
        course.code = request.code
        course.name = request.name
        course.description = request.description
        course.updated_at = datetime.now()
        course.updated_by = userid
        db.commit()

        return {
            "message": f"Course  with code {course.code} updated successfully",
            "data": {
                "code": course.code,
                "name": course.name,
                "description": course.description,
                "created_at": course.created_at,
                "created_by": course.created_by,
                "updated_at": course.updated_at,
                "updated_by": course.updated_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"Course does not exists!")


@router.delete("/{id}")
async def delete(id: UUID4, db: Session = Depends(get_db),current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    course = db.query(Course).filter(Course.id == id, Course.deleted_at == None).first()


    if course:
        course.deleted_at = datetime.now()
        course.deleted_by = userid
        db.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Course does not exists!")
