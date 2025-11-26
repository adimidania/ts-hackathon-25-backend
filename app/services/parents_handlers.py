from re import I
from cycler import V
from regex import F
from ..models.parent import Parent
from ..utils.db_setup import db,obj_id
from ..utils.auth import hash_password,verify_password
from .exceptions import ParentAlreadyExists, ParentNotFound, IncorrectPassword

async def find_parent_by_email(email: str):
    parent = await db.parents.find_one({"email": email})
    return obj_id(parent)

async def register_parent(email: str, full_name: str, phone_number: str, password: str):
    hashed_password = hash_password(password)
    if await find_parent_by_email(email):
        raise ParentAlreadyExists()
    res = await db.parents.insert_one({
        "email": email,
        "full_name": full_name,
        "phone_number": phone_number,
        "hashed_password": hashed_password,
        "stories": [],
        "drafts": []
    })
    return {"id": str(res.inserted_id)}

async def login(email: str, password: str):
    parent = await db.parents.find_one({"email": email})
    if not parent:
        raise ParentNotFound()
    if not verify_password(password, parent["hashed_password"]):
        return IncorrectPassword()
    return {
        'data': obj_id(parent),
        "msg": "Login success"
        }


async def get_parent_stories(parent_id: str):
    parent = await db.parents.find_one({"_id": parent_id})
    story_ids = parent.get("stories", [])
    stories = await db.stories.find({"_id": {"$in": story_ids}}).to_list(len(story_ids))
    return stories
async def get_parent_drafts(parent_id: str):
    parent = await db.parents.find_one({"_id": parent_id})
    draft_ids = parent.get("drafts", [])
    drafts = await db.stories.find({"_id": {"$in": draft_ids}}).to_list(len(draft_ids))
    return drafts

async def get_parents():
    parents = await db.parents.find().to_list(100)
    return obj_id(parents)
async def get_parent(parent_id: str):
    parent = await db.parents.find_one({"_id": parent_id})
    return obj_id(parent)

async def delete_parent(parent_id: str):
    await db.parents.delete_one({"_id": parent_id})
    return {"msg": "Parent deleted"}
async def update_parent(parent_id: str, data: Parent):
    await db.parents.update_one({"_id": parent_id}, {"$set": data.dict()})
    return {"msg": "Parent updated"}