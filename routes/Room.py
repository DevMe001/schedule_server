from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from config.database import get_db
from models.Room import Room
from schemas.Room import RoomSchema
from datetime import datetime
from pydantic import UUID4
from auth.Oauth2 import get_current_user
from schemas.User import UserSchema
from models.User import User
from typing import Optional, List, Union, Dict, Any

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/get", response_model=Dict[str, Union[str, List[Dict[str, Any]]]])
# for querying all the data from Courses
async def index(page: Optional[int] = 1, limit: Optional[int] = 10, db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    offset = (page - 1) * limit
    rooms = db.query(Room).filter(Room.deleted_at == None).offset(offset).limit(limit).all()
    data = []
    if rooms:
        for room in rooms:
            data.append({
                "id": room.id,
                "room_building": room.room_building,
                "room_number": room.room_number,
                "is_lab": room.is_lab,
                "created_at": room.created_at,
                "created_by": room.created_by,
                "updated_at": room.updated_at,
                "updated_by": room.updated_by
            })
    return {
        "message": "Rooms fetched successfully",
        "data": data
    }


@router.get("/getrooms")
# for querying all the data from Courses
async def index(db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    # to query the entire created table from Courses db
    rooms = db.query(Room).filter(Room.deleted_at == None).all()
    data = []
    if rooms:
        for room in rooms:
            data.append({
                "id": room.id,
                "room_building": room.room_building,
                "room_number": room.room_number,
                "is_lab": room.is_lab,
                "created_at": room.created_at,
                "created_by": room.created_by,
                "updated_at": room.updated_at,
                "updated_by": room.updated_by
            })
    return {
        "message": "All semesters fetched successfully",
        "data": data
    }


@router.post("/post")
# para mag request ng post sa db thru api
async def store(request: RoomSchema, db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    room = db.query(Room).filter(Room.room_number == request.room_number,
                                 Room.room_building == request.room_building).first()

    if room:
        raise HTTPException(status_code=400, detail=f"Room with Room number {request.room_number} already exists!")

    try:
        room = Room(
            room_building=request.room_building,
            room_number=request.room_number,
            is_lab=request.is_lab,
            created_at=datetime.now(),
            created_by=userid
        )
        db.add(room)
        db.commit()
        return {
            "message": "Room Succesfully Added!",
            "data": {
                "room_building": room.room_building,
                "room_number": room.room_number,
                "is_lab": room.is_lab,
                "created_at": room.created_at,
                "created_by": room.created_by
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/{id}")
# For ensuring the id when accessed
async def show(id: UUID4, db: Session = Depends(get_db),
                current_user: UserSchema = Depends(get_current_user)):
    room = db.query(Room).filter(Room.id == id, Room.deleted_at == None).first()

    if room:
        return {
            "message": f"Room fetched successfully room {room.room_number}",
            "data": {
                "room_building": room.room_building,
                "room_number": room.room_number,
                "is_lab": room.is_lab,
                "created_at": room.created_at,
                "created_by": room.created_by,
                "updated_at": room.updated_at,
                "updated_by": room.updated_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"Room does not exists!")


@router.put("/{id}")
async def update(id: UUID4, request: RoomSchema, db: Session = Depends(get_db),
                 current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    room = db.query(Room).filter(Room.id == id, Room.deleted_at == None).first()

    if room:
        room.room_building = request.room_building
        room.room_number = request.room_number
        room.is_lab = request.is_lab
        room.updated_at = datetime.now()
        room.updated_by = userid
        db.commit()

        return {
            "message": f"Room detail  with number {room.room_number} updated successfully",
            "data": {
                "room_building": room.room_building,
                "room_number": room.room_number,
                "is_lab": room.is_lab,
                "created_at": room.created_at,
                "created_by": room.created_by,
                "updated_at": room.updated_at,
                "updated_by": room.updated_by
            }
        }
    else:
        raise HTTPException(status_code=404, detail=f"Room does not exists!")


@router.delete("/{id}")
async def delete(id: UUID4, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_user)):
    user = db.query(User).filter(User.email == current_user.email).first()
    # If the user is not found or some other validation
    if not user:
        raise HTTPException(status_code=404, detail="Not authenticated")

    userid = user.id
    room = db.query(Room).filter(Room.id == id, Room.deleted_at == None).first()

    if room:
        room.deleted_at = datetime.now()
        room.deleted_by = userid
        db.commit()
        return {
            "message": f"Room detail  with number {room.room_number} has been moved to trash successfully",
        }
    else:
        raise HTTPException(status_code=404, detail=f"Room does not exists!")
