from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from config.database import get_db
from models.FacultyLoading import FacultyLoading
from schemas.FacultyLoading import FacultyLoadingSchema, FacultyLoadingBulkSchema, FacultySearchSchema
from datetime import datetime
from pydantic import UUID4
from auth.Oauth2 import get_current_user
from schemas.User import UserSchema
from models.User import User
from typing import Optional, List, Union, Dict, Any

router = APIRouter(prefix="/facultyloadings", tags=["Faculty Loading"])


@router.get("/get", response_model=dict)
async def index(page: Optional[int] = 1, limit: Optional[int] = 10, db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    offset = (page - 1) * limit
    facultyloadings = db.query(FacultyLoading).filter(FacultyLoading.deleted_at == None).offset(offset).limit(
        limit).all()

    data = []
    if facultyloadings:
        for facultyloading in facultyloadings:
            data.append({
                "id": facultyloading.id,
                "acadyear_id": facultyloading.acadyear_id,
                "semester_id": facultyloading.semester_id,
                "facultyname": facultyloading.facultyname,
                "facultystatus": facultyloading.facultystatus,
                "rank": facultyloading.rank,
                "course_code": facultyloading.course_code,
                "course_description": facultyloading.course_description,
                "units": facultyloading.units,
                "lec": facultyloading.lec,
                "lab": facultyloading.lab,
                "classname": facultyloading.classname,
                "schedule": facultyloading.schedule,
                "roomname": facultyloading.roomname,
                "created_at": facultyloading.created_at,
                "created_by": facultyloading.created_by,
            })

    return {
        "message": "All created curriculums fetched successfully",
        "data": data
    }


@router.get("/getfacultyloading")
# for querying all the data from Courses
async def index(db: Session = Depends(get_db)):
    facultyloadings = db.query(FacultyLoading).filter(FacultyLoading.deleted_at == None).all()
    data = []
    if facultyloadings:
        for facultyloading in facultyloadings:
            data.append({
                "id": facultyloading.id,
                "acadyear_id": facultyloading.acadyear_id,
                "semester_id": facultyloading.semester_id,
                "facultyname": facultyloading.facultyname,
                "facultystatus": facultyloading.facultystatus,
                "rank": facultyloading.rank,
                "course_code": facultyloading.course_code,
                "course_description": facultyloading.course_description,
                "units": facultyloading.units,
                "lec": facultyloading.lec,
                "lab": facultyloading.lab,
                "classname": facultyloading.classname,
                "schedule": facultyloading.schedule,
                "roomname": facultyloading.roomname,
                "created_at": facultyloading.created_at,
                "created_by": facultyloading.created_by,
            })
    return {
        "message": "All created curriculums fetched successfully",
        "data": data
    }

@router.get("/filterfindfaculty", response_model=list[FacultyLoadingSchema])
async def findfaculty(
    search_data: FacultySearchSchema = Depends(FacultySearchSchema),
    db: Session = Depends(get_db),
):
    filters = search_data.model_dump(exclude_defaults=True)

    # Extract the additional string filter
    facultyname = search_data.facultyname

    # Add the subject code filter
    if facultyname:
        filters["facultyname"] = facultyname

    faculties = db.query(FacultyLoading).filter_by(**filters).all()

    # Convert UUIDs to strings in the response
    response_data = [
        {
            **faculty.__dict__,
            "acadyear_id": str(faculty.acadyear_id),
            "semester_id": str(faculty.semester_id),
        }
        for faculty in faculties
    ]

    return response_data



@router.post("/post")
async def store_bulk(request: FacultyLoadingBulkSchema, db: Session = Depends(get_db),
                     current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    try:
        for facultyloading_data in request.facultyloadings:
            facultyloading = FacultyLoading(
                acadyear_id=facultyloading_data.acadyear_id,
                semester_id=facultyloading_data.semester_id,
                facultyname=facultyloading_data.facultyname,
                facultystatus=facultyloading_data.facultystatus,
                rank=facultyloading_data.rank,
                course_code=facultyloading_data.course_code,
                course_description=facultyloading_data.course_description,
                units=facultyloading_data.units,
                lec=facultyloading_data.lec,
                lab=facultyloading_data.lab,
                classname=facultyloading_data.classname,
                schedule=facultyloading_data.schedule,
                roomname=facultyloading_data.roomname,
                created_at=datetime.now(),
                created_by=user.id
            )
            db.add(facultyloading)

        db.commit()
        return {
            "message": "Successfully Added!",
            "data": [facultyloading.id for facultyloading in
                     db.query(FacultyLoading).order_by(FacultyLoading.created_at.desc()).limit(
                         len(request.facultyloadings)).all()]
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{id}")
# For ensuring the id when accessed
async def show(id: UUID4, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    facultyloading = db.query(FacultyLoading).filter(FacultyLoading.id == id,
                                                     FacultyLoading.deleted_at == None).first()

    if facultyloading:
        return {
            "message": f"{facultyloading.name} level fetched successfully !",
            "data": {
                "id": facultyloading.id,
                "acadyear_id": facultyloading.acadyear_id,
                "semester_id": facultyloading.semester_id,
                "facultyname": facultyloading.facultyname,
                "facultystatus": facultyloading.facultystatus,
                "rank": facultyloading.rank,
                "course_code": facultyloading.course_code,
                "course_description": facultyloading.course_description,
                "units": facultyloading.units,
                "lec": facultyloading.lec,
                "lab": facultyloading.lab,
                "classname": facultyloading.classname,
                "schedule": facultyloading.schedule,
                "roomname": facultyloading.roomname,
                "created_at": facultyloading.created_at,
                "created_by": facultyloading.created_by,
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"faculty does not exists!")


@router.delete("/{id}")
async def delete(id: UUID4, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    facultyloading = db.query(FacultyLoading).filter(FacultyLoading.id == id,
                                                     FacultyLoading.deleted_at == None).first()

    if facultyloading:
        facultyloading.deleted_at = datetime.now()
        facultyloading.deleted_by = userid
        db.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Faculty level does not Exists!")
