from fastapi import APIRouter, HTTPException, status

from app.models.parent import Parent
from app.services.exceptions import IncorrectPassword, ParentNotFound,ParentAlreadyExists

from ..services.parents_handlers import (
    register_parent,
    login,
    get_parent_stories,
    get_parent_drafts,
    get_parents,
    get_parent,
    delete_parent,
    update_parent,
)
from ..models.requests import LoginParentRequest,RegisterParentRequest
router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_parent_route(data: RegisterParentRequest):
    try:
        res = await register_parent(data.email, data.full_name,data.phone_number, data.password)
        return res
    except ParentAlreadyExists as ve:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(ve))
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login")
async def login_route(LoginData:LoginParentRequest):
    try:
        print("Login attempt for email:", LoginData.email)
        res = await login(LoginData.email, LoginData.password)
        return res
    except ParentNotFound as pe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(pe))
       
    except IncorrectPassword as ie:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ie))
         
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{parent_id}/stories")
async def get_parent_stories_route(parent_id: str):
    try:
        stories = await get_parent_stories(parent_id)
        if stories is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parent not found")
        return stories
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{parent_id}/drafts")
async def get_parent_drafts_route(parent_id: str):
    try:
        drafts = await get_parent_drafts(parent_id)
        if drafts is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parent not found")
        return drafts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


## generic
@router.get("/")
async def get_parents_route():
    try:
        parents = await get_parents()
        if not parents:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No parents found")
        return parents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{parent_id}")
async def get_parent_route(parent_id: str):
    try:
        parent = await get_parent(parent_id)
        if not parent:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parent not found")
        return parent
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{parent_id}")
async def delete_parent_route(parent_id: str):
    try:
        res = await delete_parent(parent_id)
        if res.get("deleted_count", 0) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parent not found")
        return {"msg": "Parent deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{parent_id}")
async def update_parent_route(parent_id: str, data: Parent):
    try:
        res = await update_parent(parent_id, data)
        if res.get("modified_count", 0) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parent not found")
        return {"msg": "Parent updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
