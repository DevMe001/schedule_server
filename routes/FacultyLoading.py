from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, or_, and_
from sqlalchemy.orm import Session
from config.database import get_db
from models.FacultyLoading import FacultyLoading
from schemas.FacultyLoading import FacultyLoadingSchema, FacultyLoadingBulkSchema, FacultySearchSchema, \
    SearchRoomWithFaculty, FacultyscheduleDay
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
                "facultyid": facultyloading.facultyid,
                "facultystatus": facultyloading.facultystatus,
                "totalunits": facultyloading.totalunits,
                "totalhours": facultyloading.totalhours,
                "ts": facultyloading.ts,
                "rank": facultyloading.rank,
                "course_code": facultyloading.course_code,
                "course_description": facultyloading.course_description,
                "units": facultyloading.units,
                "lec": facultyloading.lec,
                "lab": facultyloading.lab,
                "tuition_hours": facultyloading.tuition_hours,
                "day": facultyloading.day,
                "fstart_time": facultyloading.fstart_time,
                "fend_time": facultyloading.fend_time,
                "classname": facultyloading.classname,
                "roomname": facultyloading.roomname,
            })

    return {
        "message": "All created curriculums fetched successfully",
        "data": data
    }


@router.get("/getfacultyloading")
# for querying all the data from Courses
async def index(db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    facultyloadings = db.query(FacultyLoading).filter(FacultyLoading.deleted_at == None).all()
    data = []
    if facultyloadings:
        for facultyloading in facultyloadings:
            data.append({
                "id": facultyloading.id,
                "acadyear_id": facultyloading.acadyear_id,
                "semester_id": facultyloading.semester_id,
                "facultyid": facultyloading.facultyid,
                "facultystatus": facultyloading.facultystatus,
                "totalunits": facultyloading.totalunits,
                "totalhours": facultyloading.totalhours,
                "ts": facultyloading.ts,
                "rank": facultyloading.rank,
                "course_code": facultyloading.course_code,
                "course_description": facultyloading.course_description,
                "units": facultyloading.units,
                "lec": facultyloading.lec,
                "lab": facultyloading.lab,
                "tuition_hours": facultyloading.tuition_hours,
                "day": facultyloading.day,
                "fstart_time": facultyloading.fstart_time,
                "fend_time": facultyloading.fend_time,
                "classname": facultyloading.classname,
                "roomname": facultyloading.roomname,
            })
    return {
        "message": "All created curriculums fetched successfully",
        "data": data
    }


@router.get("/findroomwithfaculty", response_model=list[FacultyLoadingSchema])
async def findroom(
        filter_data: SearchRoomWithFaculty = Depends(SearchRoomWithFaculty),
        db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    filters = filter_data.model_dump(exclude_defaults=True)

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


@router.get("/findschedforday", response_model=list[FacultyLoadingSchema])
async def findschedforday(
        search_data: FacultyscheduleDay = Depends(FacultyscheduleDay),
        db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    filters = search_data.model_dump(exclude_defaults=True)

    # Apply the filter outside the filter_by method
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


@router.get("/filterfindfaculty", response_model=list[FacultyLoadingSchema])
async def findfaculty(
        search_data: FacultySearchSchema = Depends(FacultySearchSchema),
        db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    filters = search_data.model_dump(exclude_defaults=True)

    # Extract the additional integer filter
    facultyid = search_data.facultyid

    # Add the facultyid filter
    if facultyid is not None:
        filters["facultyid"] = facultyid

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
            # Check for conflicting schedules
            conflicting_schedule = db.query(FacultyLoading).filter(
                FacultyLoading.acadyear_id == facultyloading_data.acadyear_id,
                FacultyLoading.semester_id == facultyloading_data.semester_id,
                FacultyLoading.facultyid == facultyloading_data.facultyid,
                FacultyLoading.day == facultyloading_data.day,
                or_(
                    and_(
                        FacultyLoading.fstart_time < facultyloading_data.fend_time,
                        FacultyLoading.fend_time > facultyloading_data.fstart_time
                    ),
                    and_(
                        FacultyLoading.fstart_time >= facultyloading_data.fend_time,
                        FacultyLoading.fend_time <= facultyloading_data.fstart_time
                    )
                )
            ).first()

            if conflicting_schedule:
                raise HTTPException(status_code=400, detail="Conflicting schedule found.")

            # Check for uniqueness based on acadyearid, semester, course code, start time, end time, day, and room
            duplicate_schedule = db.query(FacultyLoading).filter(
                FacultyLoading.acadyear_id == facultyloading_data.acadyear_id,
                FacultyLoading.semester_id == facultyloading_data.semester_id,
                FacultyLoading.course_code == facultyloading_data.course_code,
                FacultyLoading.day == facultyloading_data.day,
                FacultyLoading.fstart_time == facultyloading_data.fstart_time,
                FacultyLoading.fend_time == facultyloading_data.fend_time,
                FacultyLoading.roomname == facultyloading_data.roomname
            ).first()

            if duplicate_schedule:
                raise HTTPException(status_code=400, detail="Class already scheduled to other Faculty member!.")

            # If no conflicts or duplicates, proceed to add the schedule
            facultyloading = FacultyLoading(
                acadyear_id=facultyloading_data.acadyear_id,
                semester_id=facultyloading_data.semester_id,
                facultyid=facultyloading_data.facultyid,
                facultystatus=facultyloading_data.facultystatus,
                totalunits=facultyloading_data.totalunits,
                totalhours=facultyloading_data.totalhours,
                ts=facultyloading_data.ts,
                rank=facultyloading_data.rank,
                course_code=facultyloading_data.course_code,
                course_description=facultyloading_data.course_description,
                units=facultyloading_data.units,
                lec=facultyloading_data.lec,
                lab=facultyloading_data.lab,
                tuition_hours=facultyloading_data.tuition_hours,
                day=facultyloading_data.day,
                fstart_time=facultyloading_data.fstart_time,
                fend_time=facultyloading_data.fend_time,
                classname=facultyloading_data.classname,
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
    except HTTPException:
        db.rollback()
        raise  # Re-raise the HTTPException
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
                "facultyid": facultyloading.facultyid,
                "facultystatus": facultyloading.facultystatus,
                "totalunits": facultyloading.totalunits,
                "totalhours": facultyloading.totalhours,
                "ts": facultyloading.ts,
                "rank": facultyloading.rank,
                "course_code": facultyloading.course_code,
                "course_description": facultyloading.course_description,
                "units": facultyloading.units,
                "lec": facultyloading.lec,
                "lab": facultyloading.lab,
                "tuition_hours": facultyloading.tuition_hours,
                "day": facultyloading.day,
                "fstart_time": facultyloading.fstart_time,
                "fend_time": facultyloading.fend_time,
                "classname": facultyloading.classname,
                "roomname": facultyloading.roomname,
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"faculty does not exists!")


@router.put("/{id}")
async def put(id: UUID4, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    facultyloading = db.query(FacultyLoading).filter(FacultyLoading.id == id,
                                                     FacultyLoading.deleted_at == None).first()

    if facultyloading:
        # Update schedule fields based on the request
        facultyloading.acadyear_id = facultyloading.acadyear_id
        facultyloading.semester_id = facultyloading.semester_id,
        facultyloading.facultyid = facultyloading.facultyid,
        facultyloading.facultystatus = facultyloading.facultystatus,
        facultyloading.totalunits = facultyloading.totalunits,
        facultyloading.totalhours = facultyloading.totalhours,
        facultyloading.ts = facultyloading.ts,
        facultyloading.rank = facultyloading.rank,
        facultyloading.course_code = facultyloading.course_code,
        facultyloading.course_description = facultyloading.course_description,
        facultyloading.units = facultyloading.units,
        facultyloading.lec = facultyloading.lec,
        facultyloading.lab = facultyloading.lab,
        facultyloading.tuition_hours = facultyloading.tuition_hour,
        facultyloading.day = facultyloading.day,
        facultyloading.fstart_time = facultyloading.fstart_time,
        facultyloading.fend_time = facultyloading.fend_time,
        facultyloading.classname = facultyloading.classname,
        facultyloading.roomname = facultyloading.roomname,
        facultyloading.updated_by = userid
        db.commit()

        return {
            "message": f"Schedule with ID {facultyloading.id} has been updated successfully",
            "data": {
                "acadyear_id": facultyloading.acadyear_id,
                "semester_id": facultyloading.semester_id,
                "facultyid": facultyloading.facultyid,
                "facultystatus": facultyloading.facultystatus,
                "totalunits": facultyloading.totalunits,
                "totalhours": facultyloading.totalhours,
                "ts": facultyloading.ts,
                "rank": facultyloading.rank,
                "course_code": facultyloading.course_code,
                "course_description": facultyloading.course_description,
                "units": facultyloading.units,
                "lec": facultyloading.lec,
                "lab": facultyloading.lab,
                "tuition_hours": facultyloading.tuition_hours,
                "day": facultyloading.day,
                "fstart_time": facultyloading.fstart_time,
                "fend_time": facultyloading.fend_time,
                "classname": facultyloading.classname,
                "roomname": facultyloading.roomname,
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"Faculty with ID {id} does not exist!")


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
