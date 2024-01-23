# routers/Curriculum.py
from fastapi import APIRouter, Depends, HTTPException, Request, Query, Path
from sqlalchemy.orm import Session, joinedload, QueryContext
from sqlalchemy import text
from config.database import get_db
from models.Curriculum import Curriculum
from schemas.AdvanceSearch import AdvancedSearchQuery
from schemas.Curriculum import CurriculumSchema, BulkCurriculumSchema, CurriculumFilterSchema, CurriculumFilterAllSchema, CurriculumSearchSubjectCode
from datetime import datetime
from pydantic import UUID4
from auth.Oauth2 import get_current_user
from schemas.User import UserSchema
from models.User import User
from typing import Optional, List, Union, Dict, Any
from uuid import UUID
import uuid
from schemas.AcademicYear import AcademicYearSchema
from uuid import UUID as UUID4

router = APIRouter(prefix="/curriculums", tags=["Curriculum"])


@router.get("/get")
async def index(db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    curriculums = db.query(Curriculum).filter(Curriculum.deleted_at == None).all()
    data = []
    if curriculums:
        for curriculum in curriculums:
            data.append({
                "id": curriculum.id,
                "curriculum_year_name": curriculum.curriculum_year_name,
                "course_id": curriculum.course_id,
                "year_level_id": curriculum.year_level_id,
                "semester_id": curriculum.semester_id,
                "subject_code": curriculum.subject_code,
                "subject_name": curriculum.subject_name,
                "pre_req": curriculum.pre_req,
                "co_req": curriculum.co_req,
                "lecture_hours": curriculum.lecture_hours,
                "lab_hours": curriculum.lab_hours,
                "units": curriculum.units,
                "tuition_hours": curriculum.tuition_hours,
                "created_at": curriculum.created_at,
                "created_by": curriculum.created_by,
                "updated_at": curriculum.updated_at,
                "updated_by": curriculum.updated_by
            })
    return {
        "message": "All curriculums fetched successfully",
        "data": data
    }


@router.post("/post")
async def store_bulk(request: BulkCurriculumSchema, db: Session = Depends(get_db),
                     current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    try:
        for curriculum_data in request.curricula:
            curriculum = Curriculum(
                curriculum_year_name=curriculum_data.curriculum_year_name,
                course_id=curriculum_data.course_id,
                year_level_id=curriculum_data.year_level_id,
                semester_id=curriculum_data.semester_id,
                subject_code=curriculum_data.subject_code,
                subject_name=curriculum_data.subject_name,
                pre_req=curriculum_data.pre_req,
                co_req=curriculum_data.co_req,
                lecture_hours=curriculum_data.lecture_hours,
                lab_hours=curriculum_data.lab_hours,
                units=curriculum_data.units,
                tuition_hours=curriculum_data.tuition_hours,
                created_at=datetime.now(),
                created_by=user.id
            )
            db.add(curriculum)

        db.commit()
        return {
            "message": "Successfully Added!",
            "data": [curriculum.id for curriculum in
                     db.query(Curriculum).order_by(Curriculum.created_at.desc()).limit(len(request.curricula)).all()]
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/filtercuri", response_model=list[CurriculumSchema])
async def get_curriculums(
        filter_data: CurriculumFilterSchema = Depends(CurriculumFilterSchema),
        db: Session = Depends(get_db),
):
    filters = filter_data.model_dump(exclude_defaults=True)

    curriculums = db.query(Curriculum).filter_by(**filters).all()

    # Convert UUIDs to strings in the response
    response_data = [
        {
            **curriculum.__dict__,
            "curriculum_year_name": str(curriculum.curriculum_year_name),
            "course_id": str(curriculum.course_id),
            "year_level_id": str(curriculum.year_level_id),
            "semester_id": str(curriculum.semester_id),
        }
        for curriculum in curriculums
    ]

    return response_data


@router.get("/findcuri", response_model=list[CurriculumSchema])
async def get_curriculumcodeyear(
        filter_data: CurriculumFilterAllSchema = Depends(CurriculumFilterAllSchema),
        db: Session = Depends(get_db),
):
    filters = filter_data.model_dump(exclude_defaults=True)

    curriculums = db.query(Curriculum).filter_by(**filters).all()

    # Convert UUIDs to strings in the response
    response_data = [
        {
            **curriculum.__dict__,
            "curriculum_year_name": str(curriculum.curriculum_year_name),
            "course_id": str(curriculum.course_id),
            "year_level_id": str(curriculum.year_level_id),
            "semester_id": str(curriculum.semester_id),
        }
        for curriculum in curriculums
    ]

    return response_data


@router.get("/filtercuri-by-subject-code", response_model=list[CurriculumSchema])
async def filter_curriculums_by_subject_code(
    search_data: CurriculumSearchSubjectCode = Depends(CurriculumSearchSubjectCode),
    db: Session = Depends(get_db),
):
    filters = search_data.model_dump(exclude_defaults=True)

    # Extract the additional string filter
    subject_code = search_data.subject_code

    # Add the subject code filter
    if subject_code:
        filters["subject_code"] = subject_code

    curriculums = db.query(Curriculum).filter_by(**filters).all()

    # Convert UUIDs to strings in the response
    response_data = [
        {
            **curriculum.__dict__,
            "curriculum_year_name": str(curriculum.curriculum_year_name),
            "course_id": str(curriculum.course_id),
            "year_level_id": str(curriculum.year_level_id),
            "semester_id": str(curriculum.semester_id),
        }
        for curriculum in curriculums
    ]

    return response_data



@router.get("/{id}")
async def show(id: UUID4, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    curriculum = db.query(Curriculum).filter(Curriculum.id == id, Curriculum.deleted_at == None).first()

    if curriculum:
        return {
            "message": f"Curriculum information fetched successfully!",
            "data": {
                "id": curriculum.id,
                "curriculum_year_name": curriculum.curriculum_year_name,
                "course_id": curriculum.course_id,
                "year_level_id": curriculum.year_level_id,
                "semester_id": curriculum.semester_id,
                "subject_code": curriculum.subject_code,
                "subject_name": curriculum.subject_name,
                "pre_req": curriculum.pre_req,
                "co_req": curriculum.co_req,
                "lecture_hours": curriculum.lecture_hours,
                "lab_hours": curriculum.lab_hours,
                "units": curriculum.units,
                "tuition_hours": curriculum.tuition_hours,
                "created_at": curriculum.created_at,
                "created_by": curriculum.created_by,
                "updated_at": curriculum.updated_at,
                "updated_by": curriculum.updated_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail="Curriculum does not exist!")


@router.put("/{id}")
async def update(id: UUID4, request: CurriculumSchema, db: Session = Depends(get_db),
                 current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    curriculum = db.query(Curriculum).filter(Curriculum.id == id, Curriculum.deleted_at == None).first()

    if curriculum:
        curriculum.curriculum_year_name = request.curriculum_year_name
        curriculum.course_id = request.course_id
        curriculum.year_level_id = request.year_level_id
        curriculum.semester_id = request.semester_id
        curriculum.subject_code = request.subject_code
        curriculum.subject_name = request.subject_name
        curriculum.pre_req = request.pre_req
        curriculum.co_req = request.co_req
        curriculum.lecture_hours = request.lecture_hours
        curriculum.lab_hours = request.lab_hours
        curriculum.units = request.units
        curriculum.tuition_hours = request.tuition_hours
        curriculum.updated_at = datetime.now()
        curriculum.updated_by = userid
        db.commit()

        return {
            "message": f"Curriculum information for {curriculum.id} has been updated successfully",
            "data": {
                "id": curriculum.id,
                "curriculum_year_name": curriculum.curriculum_year_name,
                "course_id": curriculum.course_id,
                "year_level_id": curriculum.year_level_id,
                "semester_id": curriculum.semester_id,
                "subject_code": curriculum.subject_code,
                "subject_name": curriculum.subject_name,
                "pre_req": curriculum.pre_req,
                "co_req": curriculum.co_req,
                "lecture_hours": curriculum.lecture_hours,
                "lab_hours": curriculum.lab_hours,
                "units": curriculum.units,
                "tuition_hours": curriculum.tuition_hours,
                "created_at": curriculum.created_at,
                "created_by": curriculum.created_by,
                "updated_at": curriculum.updated_at,
                "updated_by": curriculum.updated_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail="Curriculum does not exist!")


@router.delete("/{id}")
async def delete(id: UUID4, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    curriculum = db.query(Curriculum).filter(Curriculum.id == id, Curriculum.deleted_at == None).first()

    if curriculum:
        curriculum.deleted_at = datetime.now()
        curriculum.deleted_by = userid
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Curriculum does not exist!")
