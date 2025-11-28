from ..utils.db_setup import db, obj_id
from bson import ObjectId
from .exceptions import StoryNotFound
from .parents_handlers import find_parent_by_email
async def find_story_by_id(story_id: str):
    story = await db.stories.find_one({"_id": ObjectId(story_id)})
    if not story:
        raise  StoryNotFound()
    return obj_id(story)

async def create_story(email, title, paragraph):
    # 1. Insert story
    res = await db.stories.insert_one({
        "title": title,
        "paragraph": paragraph,
        "is_draft":False
    })

    story_id = res.inserted_id  

    await db.parents.update_one(
        {"email": email},
        {"$push": {"stories": story_id}}
    )

    return str(story_id)

async def get_all_stories():
    stories = await db.stories.find().to_list(100)
    return [obj_id(story) for story in stories]

async def update_story(story_id: str, update_data: dict):
    await db.stories.update_one({"_id": ObjectId(story_id)}, {"$set": update_data})
    return await find_story_by_id(story_id)
async def delete_story(story_id: str):
    await db.stories.delete_one({"_id": ObjectId(story_id)})
    return {"msg": "Story deleted"}

async def make_draft_story(story_id: str):
    await db.stories.update_one({"_id": ObjectId(story_id)}, {"$set": {"is_draft": False}})
    return await find_story_by_id(story_id)

async def story_images(story_id:str):
    story= await find_story_by_id()
    if not story:
        raise StoryNotFound()
    