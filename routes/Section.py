from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.Section import Section
from schemas.Section import SectionSchema
from datetime import datetime
from pydantic import UUID4
from typing import Optional, List, Union, Dict, Any
from auth.Oauth2 import get_current_user
from schemas.User import UserSchema
from models.User import User

router = APIRouter(prefix="/sections", tags=["Section"])


@router.get("/get", response_model=Dict[str, Union[str, List[Dict[str, Any]]]])
# for querying all the data from Courses
async def index(page: Optional[int] = 1, limit: Optional[int] = 10, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    offset = (page - 1) * limit
    # to query the entire created table from Courses db
    sections = db.query(Section).filter(Section.deleted_at==None).offset(offset).limit(limit).all()
    data =[]
    if sections:
        for section in sections:
            data.append({
                "id": section.id,
                "name": section.name,
                "order": section.order,
                "description": section.description,
                "created_at": section.created_at,
                "created_by": section.created_by,
                "updated_at": section.updated_at,
                "updated_by": section.updated_by
            })
    return{
        "message": "All section fetched successfully",
        "data": data
    }

@router.get("/getsection")
# for querying all the data from Courses
async def index(db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    # to query the entire created table from Courses db
    sections = db.query(Section).filter(Section.deleted_at == None).all()
    data = []
    if sections:
        for section in sections:
            data.append({
                "id": section.id,
                "name": section.name,
                "order": section.order,
                "description": section.description,
                "created_at": section.created_at,
                "created_by": section.created_by,
                "updated_at": section.updated_at,
                "updated_by": section.updated_by
            })
    return {
        "message": "Course fetched successfully",
        "data": data
    }







@router.post("/post")
# para mag request ng post sa db thru api
async def store(request: SectionSchema, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    section = db.query(Section).filter(Section.name == request.name).all()

    if section:
        raise HTTPException(status_code=400, detail=f"{request.name} already exists!")

    try:
        section = Section(
            name=request.name,
            order=request.order,
            description=request.description,
            created_at=datetime.now(),
            created_by=userid
        )
        db.add(section)
        db.commit()
        return {
            "message": "Succesfully Added!",
            "data": {
                "name": section.name,
                "order": section.order,
                "description": section.description,
                "created_at": section.created_at,
                "created_by": section.created_by
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{id}")
# For ensuring the id when accessed
async def show(id: UUID4, db: Session = Depends(get_db),current_user: UserSchema = Depends(get_current_user)):
    section = db.query(Section).filter(Section.id == id, Section.deleted_at == None).first()

    if section:
        return {
            "message": f"{section.name} information fetched successfully !",
            "data": {
                "name": section.name,
                "order": section.order,
                "description": section.description,
                "created_at": section.created_at,
                "created_by": section.created_by,
                "updated_at": section.updated_at,
                "updated_by": section.updated_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"section does not exists!")


@router.put("/{id}")
async def update(id: UUID4, request: SectionSchema, db: Session = Depends(get_db),current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    section = db.query(Section).filter(Section.id == id, Section.deleted_at == None).first()

    if section:
        section.name = request.name
        section.order = request.order
        section.description = request.description
        section.updated_at = datetime.now()
        section.updated_by = userid
        db.commit()

        return {
            "message": f"The following information for {section.name} has been updated successfully",
            "data": {
                "name": section.name,
                "order": section.order,
                "description": section.order,
                "created_at": section.created_at,
                "created_by": section.created_by,
                "updated_at": section.updated_at,
                "updated_by": section.updated_by
            }
        }
    else:
         raise HTTPException(status_code=404, detail=f"section does not Exists!")


@router.delete("/{id}")
async def delete(id: UUID4, db: Session= Depends(get_db),current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    section = db.query(Section).filter(Section.id == id, Section.deleted_at == None).first()

    if section:
            section.deleted_at = datetime.now()
            section.deleted_by = userid
            db.commit()
    else:
        raise HTTPException(status_code=404, detail=f"section does not Exists!")