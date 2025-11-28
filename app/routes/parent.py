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


#tested
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_parent_route(data: RegisterParentRequest):
    try:
        res = await register_parent(data.email, data.full_name,data.phone_number, data.password)
        return res
    except ParentAlreadyExists as ve:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(ve))
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# tested
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

#tested
@router.get("/{email}/stories")
async def get_parent_stories_route(email: str):
    try:
        stories = await get_parent_stories(email)
       
        return stories
    except ParentNotFound as pe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(pe))
      
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{email}/drafts")
async def get_parent_drafts_route(email: str):
    try:
        drafts = await get_parent_drafts(email)
        return drafts
    except ParentNotFound as pe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(pe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


## generic
@router.get("/")
async def get_parents_route():
    try:
        parents = await get_parents()
        return parents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{email}")
async def get_parent_route(email: str):
    try:
        parent = await get_parent(email)
        return parent
    except ParentNotFound as pe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(pe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{email}")
async def delete_parent_route(email: str):
    try:
        res = await delete_parent(email)
        if res.get("deleted_count", 0) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parent not found")
        return {"msg": "Parent deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{email}")
async def update_parent_route(email: str, data: Parent):
    try:
        res = await update_parent(email, data)
        if res.get("modified_count", 0) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parent not found")
        return {"msg": "Parent updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
