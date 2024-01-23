from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.Manage_Curriculum import Manage_Curriculum
from schemas.Manage_Curriculum import Manage_CurriculumSchema
from datetime import datetime
from pydantic import UUID4
from auth.Oauth2 import get_current_user
from schemas.User import UserSchema
from models.User import User
from typing import Optional, List, Union, Dict, Any

router = APIRouter(prefix="/managecurriculums", tags=["Manage Curriculum"])


@router.get("/get", response_model=Dict[str, Union[str, List[Dict[str, Any]]]])
# for querying all the data from Courses
async def index(page: Optional[int] = 1, limit: Optional[int] = 10, db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    offset = (page - 1) * limit
    mcurriculums = db.query(Manage_Curriculum).filter(Manage_Curriculum.deleted_at == None).offset(offset).limit(
        limit).all()
    data = []
    if mcurriculums:
        for mcurriculum in mcurriculums:
            data.append({
                "id": mcurriculum.id,
                "name": mcurriculum.name,
                "order": mcurriculum.order,
                "created_at": mcurriculum.created_at,
                "created_by": mcurriculum.created_by,
                "updated_at": mcurriculum.updated_at,
                "updated_by": mcurriculum.updated_by
            })
    return {
        "message": "All created curriculums fetched successfully",
        "data": data
    }

@router.get("/getcurnames")
# for querying all the data from Courses
async def index(db: Session = Depends(get_db),current_user: UserSchema = Depends(get_current_user)):
    mcurriculums = db.query(Manage_Curriculum).filter(Manage_Curriculum.deleted_at == None).all()
    data = []
    if mcurriculums:
        for mcurriculum in mcurriculums:
            data.append({
                "id": mcurriculum.id,
                "name": mcurriculum.name,
                "order": mcurriculum.order,
                "created_at": mcurriculum.created_at,
                "created_by": mcurriculum.created_by,
                "updated_at": mcurriculum.updated_at,
                "updated_by": mcurriculum.updated_by
            })
    return {
        "message": "All created curriculums fetched successfully",
        "data": data
    }



@router.post("/post")
# para mag request ng post sa db thru api
async def store(request: Manage_CurriculumSchema, db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    mcurriculum = db.query(Manage_Curriculum).filter(Manage_Curriculum.name == request.name).all()

    if mcurriculum:
        raise HTTPException(status_code=400, detail=f"Year level {request.name} already exists!")

    try:
        mcurriculum = Manage_Curriculum(
            name=request.name,
            order=request.order,
            created_at=datetime.now(),
            created_by=userid
        )
        db.add(mcurriculum)
        db.commit()
        return {
            "message": "Succesfully Added!",
            "data": {
                "name": mcurriculum.name,
                "order": mcurriculum.order,
                "created_at": mcurriculum.created_at,
                "created_by": mcurriculum.created_by
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{id}")
# For ensuring the id when accessed
async def show(id: UUID4, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    mcurriculum = db.query(Manage_Curriculum).filter(Manage_Curriculum.id == id,
                                                     Manage_Curriculum.deleted_at == None).first()

    if mcurriculum:
        return {
            "message": f"{mcurriculum.name} level fetched successfully !",
            "data": {
                "name": mcurriculum.name,
                "order": mcurriculum.order,
                "created_at": mcurriculum.created_at,
                "created_by": mcurriculum.created_by,
                "updated_at": mcurriculum.updated_at,
                "updated_by": mcurriculum.updated_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"Year level does not exists!")


@router.put("/{id}")
async def update(id: UUID4, request: Manage_CurriculumSchema, db: Session = Depends(get_db),
                 current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    mcurriculum = db.query(Manage_Curriculum).filter(Manage_Curriculum.id == id,
                                                     Manage_Curriculum.deleted_at == None).first()

    if mcurriculum:
        mcurriculum.name = request.name
        mcurriculum.order = request.order
        mcurriculum.updated_at = datetime.now()
        mcurriculum.updated_by = userid
        db.commit()

        return {
            "message": f"Year level {mcurriculum.name} has been updated successfully",
            "data": {
                "name": mcurriculum.name,
                "order": mcurriculum.order,
                "created_at": mcurriculum.created_at,
                "created_by": mcurriculum.created_by,
                "updated_at": mcurriculum.updated_at,
                "updated_by": mcurriculum.updated_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"Curriculum name does not exists!")


@router.delete("/{id}")
async def delete(id: UUID4, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    mcurriculum = db.query(Manage_Curriculum).filter(Manage_Curriculum.id == id,
                                                     Manage_Curriculum.deleted_at == None).first()

    if mcurriculum:
        mcurriculum.deleted_at = datetime.now()
        mcurriculum.deleted_by = userid
        db.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Year level does not Exists!")
