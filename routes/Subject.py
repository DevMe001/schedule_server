from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.Subject import Subject
from schemas.Subject import SubjectSchema
from datetime import datetime
from pydantic import UUID4

router = APIRouter(prefix="/subjects", tags=["Subjects"])


@router.get("/")
# for querying all the data from Courses
async def index(db: Session = Depends(get_db)):
    # to query the entire created table from Courses db
    subjects = db.query(Subject).filter(Subject.deleted_at==None).all()
    data =[]
    if subjects:
        for subject in subjects:
            data.append({
                "id": subject.id,
                "code": subject.code,
                "name": subject.name,
                "created_at": subject.created_at,
                "created_by": subject.created_by,
                "updated_at": subject.updated_at,
                "updated_by": subject.updated_by
            })
    return{
        "message": "subjects fetched successfully",
        "data": data
    }


@router.post("/")
# para mag request ng post sa db thru api
async def store(request: SubjectSchema, db: Session = Depends(get_db)):
    subjects = db.query(Subject).filter(Subject.code == request.code).all()
    if subjects:
        raise HTTPException(status_code=400, detail=f"Course with code {request.code} already exists!")

    try:
        subjects = Subject(
            code=request.code,
            name=request.name,
            created_at=datetime.now(),
            created_by="f03619a1-08eb-42ed-8152-a48033a5e731"
        )
        db.add(subjects)
        db.commit()
        return {
            "message": "Succesfully Added!",
            "data": {
                "code": subjects.code,
                "name": subjects.name,
                "created_at": subjects.created_at,
                "created_by": subjects.created_by
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{id}")
# For ensuring the id when accessed
async def show(id: UUID4, db: Session = Depends(get_db)):
    subjects = db.query(Subject).filter(Subject.id == id, Subject.deleted_at == None).first()

    if subjects:
        return {
            "message": f"Course fetched successfully with code {subjects.code}",
            "data": {
                "code": subjects.code,
                "name": subjects.name,
                "created_at": subjects.created_at,
                "created_by": subjects.created_by,
                "updated_at": subjects.updated_at,
                "updated_by": subjects.updated_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"Subject does not exists!")


@router.put("/{id}")
async def update(id: UUID4, request: SubjectSchema, db: Session = Depends(get_db)):
    subjects = db.query(Subject).filter(Subject.id == id, Subject.deleted_at == None).first()

    if subjects:
        subjects.code = request.code
        subjects.name = request.name
        subjects.updated_at = datetime.now()
        subjects.updated_by = "f03619a1-08eb-42ed-8152-a48033a5e731"
        db.commit()

        return {
            "message": f"Course  with code {subjects.code} updated successfully",
            "data": {
                "code": subjects.code,
                "name": subjects.name,
                "created_at": subjects.created_at,
                "created_by": subjects.created_by,
                "updated_at": subjects.updated_at,
                "updated_by": subjects.updated_by
            }
        }
    else:
         raise HTTPException(status_code=404, detail=f"Subject does not exists!")


@router.delete("/{id}")
async def delete(id: UUID4, db: Session= Depends(get_db)):
        subjects = db.query(Subject).filter(Subject.id == id, Subject.deleted_at == None).first()

        if subjects:
            subjects.deleted_at = datetime.now()
            subjects.deleted_by = "f03619a1-08eb-42ed-8152-a48033a5e731"
            db.commit()
        else:
            raise HTTPException(status_code=404, detail=f"Subject does not exists!")
