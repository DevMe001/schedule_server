from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.Person import Person
from schemas.Person import PersonSchema, PersonBulkCreateSchema

router = APIRouter(prefix="/persons", tags=["Persons"])


@router.post("/")
def create_person(person_data: PersonSchema, db: Session = Depends(get_db)):
    new_person = Person(**person_data.dict(by_alias=True))
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person


@router.post("/bulk/")
def create_persons_bulk(persons_data: PersonBulkCreateSchema, db: Session = Depends(get_db)):
    new_persons = []
    for person_data in persons_data.items:
        new_person = Person(**person_data.dict(by_alias=True))
        db.add(new_person)
        new_persons.append(new_person)

    db.commit()
    return new_persons
