from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, and_, func
from sqlalchemy.orm import Session, joinedload, Load
from config.database import get_db
from models.Manage_Schedule import Manage_Schedule
from models.User import User
from schemas.Manage_Schedule import (ScheduleSchema, BulkScheduleSchema, RoomScheduleSchema, ClassScheduleFilterSchema,
                                     ScheduleSearchSubjectCode, RoomSearch, roomchartSchema)
from datetime import datetime, time
from pydantic import UUID4
from auth.Oauth2 import get_current_user
from schemas.User import UserSchema
from typing import Optional, List, Union, Dict, Any
from models.Room import Room

router = APIRouter(prefix="/manageschedules", tags=["Manage Schedules"])


@router.get("/get", response_model=Dict[str, Union[str, List[Dict[str, Any]]]])
async def index(page: Optional[int] = 1, limit: Optional[int] = 10, db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    offset = (page - 1) * limit
    schedules = db.query(Manage_Schedule).filter(Manage_Schedule.deleted_at == None).offset(offset).limit(
        limit).all()
    data = []
    if schedules:
        for schedule in schedules:
            data.append({
                "id": schedule.id,
                "acadyear_id": schedule.acadyear_id,
                "course_id": schedule.course_id,
                "semester_id": schedule.semester_id,
                "class_id": schedule.class_id,
                "subject_code": schedule.subject_code,
                "subject_name": schedule.subject_name,
                "lecture_hours": schedule.lecture_hours,
                "lab_hours": schedule.lab_hours,
                "units": schedule.units,
                "tuition_hours": schedule.tuition_hours,
                "day": schedule.day,
                "start_time": schedule.start_time.strftime("%I:%M %p"),
                "end_time": schedule.end_time.strftime("%I:%M %p"),
                "room_id": schedule.room_id,
                "created_at": schedule.created_at,
                "created_by": schedule.created_by,
                "updated_at": schedule.updated_at,
                "updated_by": schedule.updated_by
            })
    return {
        "message": "All schedules fetched successfully",
        "data": data
    }
@router.get("/getschedules")
# for querying all the data from Courses
async def index(db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    # to query the entire created table from Courses db
    schedules = db.query(Manage_Schedule).filter(Manage_Schedule.deleted_at == None).all()
    data = []
    if schedules:
        for schedule in schedules:
            data.append({
                "id": schedule.id,
                "acadyear_id": schedule.acadyear_id,
                "course_id": schedule.course_id,
                "semester_id": schedule.semester_id,
                "class_id": schedule.class_id,
                "subject_code": schedule.subject_code,
                "subject_name": schedule.subject_name,
                "lecture_hours": schedule.lecture_hours,
                "lab_hours": schedule.lab_hours,
                "units": schedule.units,
                "tuition_hours": schedule.tuition_hours,
                "day": schedule.day,
                "start_time": schedule.start_time.strftime("%I:%M %p"),
                "end_time": schedule.end_time.strftime("%I:%M %p"),
                "room_id": schedule.room_id,
                "created_at": schedule.created_at,
                "created_by": schedule.created_by,
                "updated_at": schedule.updated_at,
                "updated_by": schedule.updated_by
            })
    return {
        "message": "All schedules fetched successfully",
        "data": data
    }

@router.get("/roompiechart", response_model=list[ScheduleSchema])
async def findroomchart(
        filter_data: roomchartSchema = Depends(roomchartSchema),
        db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    filters = filter_data.model_dump(exclude_defaults=True)

    schedules = db.query(Manage_Schedule).filter_by(**filters).all()

    # Convert UUIDs to strings in the response
    response_data = [
        {
            **schedule.__dict__,
            "acadyear_id": str(schedule.acadyear_id),
            "course_id": str(schedule.course_id),
            "semester_id": str(schedule.semester_id),
            "class_id": str(schedule.class_id),
            "room_id": str(schedule.room_id),
            "room_number": schedule.room.room_number if schedule.room else None,
        }
        for schedule in schedules
    ]
    return response_data

@router.post("/post")
async def store(request: ScheduleSchema, db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    schedule = db.query(Manage_Schedule).filter(
        Manage_Schedule.subject_code == request.subject_code,
        Manage_Schedule.day == request.day,
        Manage_Schedule.start_time == request.start_time,
        Manage_Schedule.end_time == request.end_time,
        Manage_Schedule.deleted_at == None
    ).first()

    if schedule:
        raise HTTPException(status_code=400, detail=f"Schedule already exists!")

    try:
        schedule = Manage_Schedule(
            acadyear_id=request.acadyear_id,
            course_id=request.course_id,
            semester_id=request.semester_id,
            class_id=request.class_id,
            subject_code=request.subject_code,
            subject_name=request.subject_name,
            lecture_hours=request.lecture_hours,
            lab_hours=request.lab_hours,
            units=request.units,
            tuition_hours=request.tuition_hours,
            day=request.day,
            start_time=request.start_time,
            end_time=request.end_time,
            room_id=request.room_id,
            created_at=datetime.now(),
            created_by=userid
        )
        db.add(schedule)
        db.commit()
        return {
            "message": "Successfully added schedule!",
            "data": {
                "id": schedule.id,
                "subject_code": schedule.subject_code,
                "subject_name": schedule.subject_name,
                "day": schedule.day,
                "start_time": schedule.start_time.strftime("%I:%M %p"),
                "end_time": schedule.end_time.strftime("%I:%M %p"),
                "created_at": schedule.created_at,
                "created_by": schedule.created_by
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/validate-schedule")
async def validate_schedule(request: ScheduleSchema, db: Session = Depends(get_db),
                            current_user: UserSchema = Depends(get_current_user)):
    try:
        # Check for conflicting schedules
        conflicting_schedule = db.query(Manage_Schedule).filter(
            Manage_Schedule.acadyear_id == request.acadyear_id,
            Manage_Schedule.semester_id == request.semester_id,
            Manage_Schedule.room_id == request.room_id,
            Manage_Schedule.day == request.day,
            or_(
                and_(
                    Manage_Schedule.start_time < request.end_time,
                    Manage_Schedule.end_time > request.start_time
                ),
                and_(
                    Manage_Schedule.start_time >= request.end_time,
                    Manage_Schedule.end_time <= request.start_time
                )
            )
        ).first()

        if conflicting_schedule:
            raise HTTPException(status_code=400, detail="Conflicting schedule found.")

        # If no conflict, return "Validated"
        return {"message": "Validated"}

    except HTTPException as e:
        raise  # Re-raise the HTTPException
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/bulk-post")
async def bulk_store(request: BulkScheduleSchema, db: Session = Depends(get_db),
                     current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id

    try:
        for schedule_data in request.schedules:
            conflicting_schedule = db.query(Manage_Schedule).filter(
                Manage_Schedule.acadyear_id == schedule_data.acadyear_id,
                Manage_Schedule.semester_id == schedule_data.semester_id,
                Manage_Schedule.room_id == schedule_data.room_id,
                Manage_Schedule.day == schedule_data.day,
                or_(
                    and_(
                        Manage_Schedule.start_time <= schedule_data.start_time,
                        Manage_Schedule.end_time >= schedule_data.start_time
                    ),
                    and_(
                        Manage_Schedule.start_time <= schedule_data.end_time,
                        Manage_Schedule.end_time >= schedule_data.end_time
                    ),
                    and_(
                        Manage_Schedule.start_time >= schedule_data.start_time,
                        Manage_Schedule.end_time <= schedule_data.end_time
                    )
                )
            ).first()

            conflicting_request_schedule = any(
                (existing_schedule for existing_schedule in request.schedules
                 if existing_schedule != schedule_data and
                 existing_schedule.day == schedule_data.day and
                 existing_schedule.room_id == schedule_data.room_id and
                 ((existing_schedule.start_time <= schedule_data.start_time < existing_schedule.end_time) or
                  (existing_schedule.start_time < schedule_data.end_time <= existing_schedule.end_time) or
                  (schedule_data.start_time <= existing_schedule.start_time < schedule_data.end_time) or
                  (schedule_data.start_time < existing_schedule.end_time <= schedule_data.end_time))
                 )
            )

            if conflicting_schedule or conflicting_request_schedule:
                raise HTTPException(status_code=400, detail="Conflicting schedule found.")

            # If no conflict, proceed to add the schedule
            schedule = Manage_Schedule(
                acadyear_id=schedule_data.acadyear_id,
                course_id=schedule_data.course_id,
                semester_id=schedule_data.semester_id,
                class_id=schedule_data.class_id,
                subject_code=schedule_data.subject_code,
                subject_name=schedule_data.subject_name,
                lecture_hours=schedule_data.lecture_hours,
                lab_hours=schedule_data.lab_hours,
                units=schedule_data.units,
                tuition_hours=schedule_data.tuition_hours,
                day=schedule_data.day,
                start_time=schedule_data.start_time,
                end_time=schedule_data.end_time,
                room_id=schedule_data.room_id,
                created_at=datetime.now(),
                created_by=userid
            )
            db.add(schedule)

        db.commit()
        return {"message": "Bulk insert successful!"}
    except HTTPException:
        db.rollback()
        raise  # Re-raise the HTTPException
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/filtersched", response_model=list[ScheduleSchema])
async def get_curriculums(
        filter_data: ClassScheduleFilterSchema = Depends(ClassScheduleFilterSchema),
        db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    filters = filter_data.model_dump(exclude_defaults=True)

    schedules = (
        db.query(Manage_Schedule)
        .options(joinedload(Manage_Schedule.room))  # Apply joinedload to eagerly load the 'room'
        .filter_by(**filters)
        .all()
    )

    # Convert UUIDs to strings in the response
    response_data = [
        {
            **schedule.__dict__,
            "acadyear_id": str(schedule.acadyear_id),
            "course_id": str(schedule.course_id),
            "semester_id": str(schedule.semester_id),
            "class_id": str(schedule.class_id),
            "room_id": str(schedule.room_id),
            "room_number": schedule.room.room_number if schedule.room else None,
        }
        for schedule in schedules
    ]

    return response_data

@router.get("/findroom", response_model=list[ScheduleSchema])
async def get_rooms(
        filter_data: RoomSearch = Depends(RoomSearch),
        db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    filters = filter_data.model_dump(exclude_defaults=True)

    schedules = (
        db.query(Manage_Schedule)
        .options(joinedload(Manage_Schedule.room))  # Apply joinedload to eagerly load the 'room'
        .filter_by(**filters)
        .all()
    )

    # Convert UUIDs to strings in the response
    response_data = [
        {
            **schedule.__dict__,
            "acadyear_id": str(schedule.acadyear_id),
            "course_id": str(schedule.course_id),
            "semester_id": str(schedule.semester_id),
            "class_id": str(schedule.class_id),
            "room_id": str(schedule.room_id),
            "room_number": schedule.room.room_number if schedule.room else None,
        }
        for schedule in schedules
    ]

    return response_data


@router.get("/findroomscheds", response_model=list[ScheduleSchema])
async def findroomschedules(
        search_data: RoomScheduleSchema = Depends(RoomScheduleSchema),
        db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    filters = search_data.model_dump(exclude_defaults=True)

    # Extract the additional string filter
    day = search_data.day

    # Add the subject code filter
    if day:
        filters["day"] = day

    # Use options to eagerly load the Class information
    schedules = (
        db.query(Manage_Schedule)
        .filter_by(**filters)
        .options(joinedload(Manage_Schedule.classes))  # Eager load the 'classes' relationship
        .all()
    )

    # Debug prints to check schedules and their associated classes
    print('Schedules with Classes:', schedules)
    for schedule in schedules:
        class_name = None

        if schedule.classes:
            # Check if classes is a list
            if isinstance(schedule.classes, list):
                class_name = ', '.join(cls.classname for cls in schedule.classes)
            else:
                class_name = schedule.classes.classname

        print(f"Schedule ID: {schedule.id}, Class: {class_name}")

    # Convert UUIDs to strings in the response
    response_data = [
        {
            **schedule.__dict__,
            "acadyear_id": str(schedule.acadyear_id),
            "course_id": str(schedule.course_id),
            "semester_id": str(schedule.semester_id),
            "class_id": str(schedule.class_id),
            "room_id": str(schedule.room_id),
            "classname": class_name,
        }
        for schedule in schedules
    ]

    return response_data



@router.get("/filtersched-by-subject-code", response_model=list[ScheduleSchema])
async def filter_schedule_by_subject_code(
        search_data: ScheduleSearchSubjectCode = Depends(ScheduleSearchSubjectCode),
        db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    filters = search_data.model_dump(exclude_defaults=True)

    # Extract the additional string filter and convert to uppercase
    subject_code = search_data.subject_code.upper() if search_data.subject_code else None

    # Add the case-insensitive subject code filter
    if subject_code:
        filters["subject_code"] = func.upper(Manage_Schedule.subject_code)

    # Apply the filter outside the filter_by method
    schedules = db.query(Manage_Schedule).filter_by(**filters).filter(filters["subject_code"] == func.upper(subject_code)).all()

    # Convert UUIDs to strings in the response
    response_data = [
        {
            **schedule.__dict__,
            "acadyear_id": str(schedule.acadyear_id),
            "course_id": str(schedule.course_id),
            "semester_id": str(schedule.semester_id),
            "class_id": str(schedule.class_id),
            "room_id": str(schedule.room_id),
        }
        for schedule in schedules
    ]

    return response_data


@router.get("/{id}")
async def show(id: UUID4, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    schedule = db.query(Manage_Schedule).filter(Manage_Schedule.id == id,
                                                Manage_Schedule.deleted_at == None).first()

    if schedule:
        return {
            "message": f"Schedule with ID {schedule.id} fetched successfully!",
            "data": {
                "id": schedule.id,
                "acadyear_id": schedule.acadyear_id,
                "course_id": schedule.course_id,
                "semester_id": schedule.semester_id,
                "class_id": schedule.class_id,
                "subject_code": schedule.subject_code,
                "subject_name": schedule.subject_name,
                "lecture_hours": schedule.lecture_hours,
                "lab_hours": schedule.lab_hours,
                "units": schedule.units,
                "tuition_hours": schedule.tuition_hours,
                "day": schedule.day,
                "start_time": schedule.start_time.strftime("%I:%M %p"),
                "end_time": schedule.end_time.strftime("%I:%M %p"),
                "room_id": schedule.room_id,
                "created_at": schedule.created_at,
                "created_by": schedule.created_by,
                "updated_at": schedule.updated_at,
                "updated_by": schedule.updated_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"Schedule with ID {id} does not exist!")


@router.put("/{id}")
async def update(id: UUID4, request: ScheduleSchema, db: Session = Depends(get_db),
                 current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    schedule = db.query(Manage_Schedule).filter(Manage_Schedule.id == id,
                                                Manage_Schedule.deleted_at == None).first()

    if schedule:
        # Update schedule fields based on the request
        schedule.acadyear_id = request.acadyear_id
        schedule.course_id = request.course_id
        # Update other fields similarly...

        schedule.updated_at = datetime.now()
        schedule.updated_by = userid
        db.commit()

        return {
            "message": f"Schedule with ID {schedule.id} has been updated successfully",
            "data": {
                "id": schedule.id,
                "subject_code": schedule.subject_code,
                "subject_name": schedule.subject_name,
                "day": schedule.day,
                "start_time": schedule.start_time.strftime("%I:%M %p"),
                "end_time": schedule.end_time.strftime("%I:%M %p"),
                "created_at": schedule.created_at,
                "created_by": schedule.created_by,
                "updated_at": schedule.updated_at,
                "updated_by": schedule.updated_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"Schedule with ID {id} does not exist!")


@router.delete("/{id}")
async def delete(id: UUID4, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    schedule = db.query(Manage_Schedule).filter(Manage_Schedule.id == id,
                                                Manage_Schedule.deleted_at == None).first()

    if schedule:
        schedule.deleted_at = datetime.now()
        schedule.deleted_by = userid
        db.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Schedule with ID {id} does not exist!")
