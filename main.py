from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import event

import models
from routes import (Course, YearLevel, Semester, Curriculum, Room, Class, Subject,
                    User, Login, Section, Manage_Curriculum, AcademicYear, FacultyInfo, Manage_Schedule, FacultyLoading)
from config.database import engine


app = FastAPI(
    title="Scheduling System",
    version="4.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001", "http://localhost:8001", "http://172.20.10.4:8001", "*",'https://scheduler-x302.onrender.com'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
)
# seeding Courses data// Makes the system avoid any problems in backend
# ----------------------------------------------------------------------------------------------------------------------
data = {
    "courses": [
        {
            "code": "BSIT",
            "name": "Bachelor of Science in Information Technology",
            "description": "",
            "created_at": "2023-11-26 19:06:40",
            "created_by": "f03619a1-08eb-42ed-8152-a48033a5e731",
        },
        {
            "code": "BBTLEDHE",
            "name": "Bachelor of Business Technology and Livelihood Education major in Home Economics",
            "description": "",
            "created_at": "2023-11-26 19:06:40",
            "created_by": "f03619a1-08eb-42ed-8152-a48033a5e731",
        },
        {
            "code": "BTLEDICT",
            "name": "Bachelor of Business Technology and Livelihood Education major in Information Communication and "
                    "Technology",
            "description": "",
            "created_at": "2023-11-26 19:06:40",
            "created_by": "f03619a1-08eb-42ed-8152-a48033a5e731",
        },
    ],
    "year_levels": [
        {
            "name": "First year",
            "order": "1",
            "created_at": "2023-11-27 02:15:51",
            "created_by": "f03619a1-08eb-42ed-8152-a48033a5e731"
        },
        {
            "name": "Second year",
            "order": "2",
            "created_at": "2023-11-27 02:15:51",
            "created_by": "f03619a1-08eb-42ed-8152-a48033a5e731",
        },
        {
            "name": "Third year",
            "order": "3",
            "created_at": "2023-11-27 02:15:51",
            "created_by": "f03619a1-08eb-42ed-8152-a48033a5e731",
        },
    ],
    "semesters": [
        {
            "name": "First Semester",
            "order": "1",
            "created_at": "2023-11-27 02:15:51",
            "created_by": "f03619a1-08eb-42ed-8152-a48033a5e731"
        },
        {
            "name": "Second Semester",
            "order": "2",
            "created_at": "2023-11-27 02:15:51",
            "created_by": "f03619a1-08eb-42ed-8152-a48033a5e731",
        },
        {
            "name": "Third Semester",
            "order": "3",
            "created_at": "2023-11-27 02:15:51",
            "created_by": "f03619a1-08eb-42ed-8152-a48033a5e731",
        },
    ],
    "rooms": [
        {
            "room_building": "Academic Building",
            "room_number": "101",
            "is_lab": True,
            "created_at": "2023-11-30 02:15:51",
            "created_by": "f03619a1-08eb-42ed-8152-a48033a5e731"
        },
        {
            "room_building": "Academic Building",
            "room_number": "102",
            "is_lab": False,
            "created_at": "2023-11-30 02:15:51",
            "created_by": "f03619a1-08eb-42ed-8152-a48033a5e731"
        },
        {
            "room_building": "AVR Building",
            "room_number": "105",
            "is_lab": True,
            "created_at": "2023-11-30 02:15:51",
            "created_by": "f03619a1-08eb-42ed-8152-a48033a5e731"
        },
    ],
    "subjects": [
        {
            "code": "COMPROG",
            "name": "Python",
            "created_at": "2023-11-30 02:15:51",
            "created_by": "f03619a1-08eb-42ed-8152-a48033a5e731"
        },
    ]
}


def initialize_table(target, connection, **kw):
    tablename = str(target)
    if tablename in data and len(data[tablename]) > 0:
        connection.execute(target.insert(), data[tablename])


event.listen(models.Course.Course.__table__, 'after_create', initialize_table)
event.listen(models.YearLevel.YearLevel.__table__, 'after_create', initialize_table)
event.listen(models.Semester.Semester.__table__, 'after_create', initialize_table)
event.listen(models.Curriculum.Curriculum.__table__, 'after_create', initialize_table)
event.listen(models.Room.Room.__table__, 'after_create', initialize_table)
event.listen(models.Subject.Subject.__table__, 'after_create', initialize_table)


# ----------------------------------------------------------------------------------------------------------------------


@app.on_event("startup")
def configure():
    models.Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Welcome"])
async def root() -> dict:
    return {
        "message": f"Welcome to {app.title} v{app.version}."
    }


# include the routing for all the api
app.include_router(Course.router)
app.include_router(YearLevel.router)
app.include_router(Semester.router)
app.include_router(Curriculum.router)
app.include_router(Room.router)
app.include_router(Class.router)
app.include_router(Subject.router)
app.include_router(User.router)
app.include_router(Login.router)
app.include_router(Section.router)
app.include_router(Manage_Curriculum.router)
app.include_router(AcademicYear.router)
app.include_router(FacultyInfo.router)
app.include_router(Manage_Schedule.router)
app.include_router(FacultyLoading.router)


# uvicorn main:app --reload
