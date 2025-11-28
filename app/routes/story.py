from fastapi import APIRouter

from app.models.requests import GenerateStoryRequest, GenerateStoryResponse
from app.services.story_generator import StoryGenerator
from ..models.story import Story
from ..services.stories_handlers import get_stories_images
from ..utils.db_setup import db
from fastapi import HTTPException
from ..services.exceptions import StoryNotFound
router = APIRouter()




@router.get("/{story_id}/images")
async def find_images_story_route(story_id:str):
    try:
        print("getting images")
        images= await get_stories_images(story_id)
        return images

    except StoryNotFound as sf:
        raise HTTPException(status_code=404,detail=str(sf))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.post("/create")
async def create_story(story: Story):
    res = await db.stories.insert_one(story.dict())
    return {"id": str(res.inserted_id)}

@router.get("/") 
async def get_stories():
    stories = await db.stories.find().to_list(100)
    return stories

