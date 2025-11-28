from ..utils.db_setup import db, obj_id
from bson import ObjectId
from .exceptions import StoryNotFound

async def find_story_by_id(story_id: str):
    story = await db.stories.find_one({"_id": ObjectId(story_id)})
    if not story:
        raise  StoryNotFound()
    return story

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


async def get_stories_images(story_id: str):
    print('processing')
    # Pass the ID to the function
    story = await find_story_by_id(story_id)
    if not story:
        raise StoryNotFound()

    # Get the image IDs from the story document
    story_image_ids = story.get("pictures", [])
    if not story_image_ids:
        return []

    story_object_ids = [ObjectId(i) for i in story_image_ids]


    print('story image ids:', story_object_ids)

    images = await db.images.find({
        "_id": {"$in": story_object_ids},
    }).to_list(len(story_object_ids))
    
    print('images found:', images)

    def serialize_image(img):
        img["_id"] = str(img["_id"])
        return img

    return [serialize_image(img) for img in images]
