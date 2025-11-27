from fastapi import APIRouter
from ..models.parent import Parent
from ..utils.auth import hash_password
from ..utils.auth import verify_password
from ..utils.db_setup   import db

router = APIRouter(prefix="/parents")

@router.post("/register")
async def register_parent(data: Parent):
    data.hashed_password = hash_password(data.hashed_password)
    res = await db.parents.insert_one(data.dict())
    return {"id": str(res.inserted_id)}

@router.post("/login")
async def login(email: str, password: str):
    parent = await db.parents.find_one({"email": email})
    if not parent:
        return {"error": "Parent not found"}
    if not verify_password(password, parent["hashed_password"]):
        return {"error": "Invalid password"}
    return {"msg": "Login success"}
