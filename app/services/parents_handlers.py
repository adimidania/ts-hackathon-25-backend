
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

from bson import ObjectId
def serialize_story(story: dict):
    """Convert all ObjectId fields to string for JSON serialization"""
    story["_id"] = str(story["_id"])
    if "pictures" in story:
        story["pictures"] = [str(p) for p in story["pictures"]]
    if "audio" in story and isinstance(story["audio"], ObjectId):
        story["audio"] = str(story["audio"])
    return story

def convert_to_objectid_list(ids):
    """Safely convert a list of strings/ObjectIds to ObjectIds"""
    object_ids = []
    for i in ids:
        if isinstance(i, ObjectId):
            object_ids.append(i)
        elif isinstance(i, str) and ObjectId.is_valid(i):
            object_ids.append(ObjectId(i))
    return object_ids

async def get_parent_stories(email: str):
    parent = await db.parents.find_one({"email": email})
    if not parent:
        raise ParentNotFound("Parent not found")

    story_ids = convert_to_objectid_list(parent.get("stories", []))
    print(story_ids)

    stories = await db.stories.find({
        "_id": {"$in": story_ids},
        "is_draft": False
    }).to_list(len(story_ids))

    return [serialize_story(s) for s in stories]

async def get_parent_drafts(email: str):
    parent = await db.parents.find_one({"email": email})
    if not parent:
        raise ParentNotFound("Parent not found")

    story_ids = convert_to_objectid_list(parent.get("drafts", []))
    print(story_ids)

    stories = await db.stories.find({
        "_id": {"$in": story_ids},
        "is_draft": True
    }).to_list(len(story_ids))

    return [serialize_story(s) for s in stories]




async def get_parents():
    parents = await db.parents.find().to_list(100)
    return obj_id(parents)

async def get_parent(email: str):
    parent = await db.parents.find_one({"email": email})
    if not parent:
        raise ParentNotFound()
    return obj_id(parent)


async def delete_parent(email: str):
    parent=get_parent(email) # make sure the parent exists
    await db.parents.delete_one({"email": email})
    return {"msg": "Parent deleted"}


async def update_parent(email: str, data: Parent):
    parent=get_parent(email)
    update=await db.parents.update_one({"email": email}, {"$set": data.dict()})
    return {"msg": "Parent updated"}