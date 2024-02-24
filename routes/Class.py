# routers/Curriculum.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from config.database import get_db
from models.Class import Class
from schemas.Class import ClassSchema
from datetime import datetime
from pydantic import UUID4
from auth.Oauth2 import get_current_user
from schemas.User import UserSchema
from models.User import User
from typing import Optional, List, Union, Dict, Any

router = APIRouter(prefix="/classes", tags=["Classes"])


@router.get("/get", response_model=Dict[str, Union[str, List[Dict[str, Any]]]])
async def index(page: Optional[int] = 1, limit: Optional[int] = 10, db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    # Calculate the offset based on page and limit
    offset = (page - 1) * limit

    # Use joinedload to fetch related data from other tables
    classes = (
        db.query(Class)
        .options(
            joinedload(Class.year_level_classec),
            joinedload(Class.course),
            joinedload(Class.section),
        )
        .filter(Class.deleted_at == None)
        .offset(offset)
        .limit(limit)
        .all()
    )

    data = []
    if classes:
        for classs in classes:
            data.append({
                "id": classs.id,
                "classname": classs.classname,
                "year_level_id": classs.year_level_id,
                "course_id": classs.course_id,
                "section_id": classs.section_id,
                "course_name": classs.course.name,  # Access related data
                "year_level_name": classs.year_level_classec.name,  # Access related data
                "section_name": classs.section.name,  # Access related data
                "created_at": classs.created_at,
                "created_by": classs.created_by,
                "updated_at": classs.updated_at,
                "updated_by": classs.updated_by
            })
    return {
        "message": "All Classes fetched successfully",
        "data": data
    }
@router.get("/getclass")
# for querying all the data from Courses
async def index(db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    # to query the entire created table from Courses db
    classes = db.query(Class).filter(Class.deleted_at == None).all()
    data = []
    if classes:
        for classs in classes:
            data.append({
                "id": classs.id,
                "classname": classs.classname,
                "year_level_id": classs.year_level_id,
                "course_id": classs.course_id,
                "section_id": classs.section_id,
                "created_at": classs.created_at,
                "created_by": classs.created_by,
                "updated_at": classs.updated_at,
                "updated_by": classs.updated_by
            })
    return {
        "message": "Course fetched successfully",
        "data": data
    }


@router.post("/post")
async def store(request: ClassSchema, db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    classs = db.query(Class).filter(Class.classname == request.classname, Class.deleted_at == None).first()

    if classs:
        raise HTTPException(status_code=400, detail="Class already exists!")

    try:
        classs = Class(
            classname=request.classname,
            year_level_id=request.year_level_id,
            course_id=request.course_id,
            section_id=request.section_id,
            created_at=datetime.now(),
            created_by=userid
        )
        db.add(classs)
        db.commit()
        return {
            "message": "Successfully Added!",
            "data": {
                "id": classs.id,
                "classname": classs.classname,
                "year_level_id": classs.year_level_id,
                "course_id": classs.course_id,
                "section_id": classs.section_id,
                "created_at": classs.created_at,
                "created_by": classs.created_by
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{id}")
async def show(id: UUID4, db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    classs = db.query(Class).filter(Class.id == id, Class.deleted_at == None).first()

    if classs:
        return {
            "message": f"Class information fetched successfully!",
            "data": {
                "id": classs.id,
                "classname": classs.classname,
                "year_level_id": classs.year_level_id,
                "course_id": classs.course_id,
                "section_id": classs.section_id,
                "created_at": classs.created_at,
                "created_by": classs.created_by,
                "updated_at": classs.updated_at,
                "updated_by": classs.updated_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail="Class does not exist!")


@router.put("/{id}")
async def update(id: UUID4, request: ClassSchema, db: Session = Depends(get_db),current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    classs = db.query(Class).filter(Class.id == id, Class.deleted_at == None).first()

    if classs:
        classs.classname = request.classname,
        classs.year_level_id = request.year_level_id
        classs.course_id = request.course_id
        classs.section_id = request.section_id
        classs.updated_at = datetime.now()
        classs.updated_by = userid
        db.commit()

        return {
            "message": "Class information has been updated successfully",
            "data": {
                "id": classs.id,
                "classname": classs.classname,
                "year_level_id": classs.year_level_id,
                "course_id": classs.course_id,
                "section_id": classs.section_id,
                "created_at": classs.created_at,
                "created_by": classs.created_by,
                "updated_at": classs.updated_at,
                "updated_by": classs.updated_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail="Class does not exist!")


@router.delete("/{id}")
async def delete(id: UUID4, db: Session = Depends(get_db),current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    classs = db.query(Class).filter(Class.id == id, Class.deleted_at == None).first()

    if classs:
        classs.deleted_at = datetime.now()
        classs.deleted_by = userid
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Class does not exist!")