from ..utils.db_setup import db, obj_id
from bson import ObjectId

async def find_story_by_id(story_id: str):
    story = await db.stories.find_one({"_id": ObjectId(story_id)})
    if not story:
        return None
    return obj_id(story)

async def create_story(story_data: dict):
    res = await db.stories.insert_one(story_data)
    return str(res.inserted_id)
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
