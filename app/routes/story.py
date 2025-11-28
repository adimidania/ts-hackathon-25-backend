from fastapi import APIRouter

from app.models.requests import GenerateStoryRequest, GenerateStoryResponse, StoryCreationRequest
from app.services.story_generator import StoryGenerator
from ..models.story import Story
from app.services.stories_handlers import create_story
from ..utils.db_setup import db

router = APIRouter()


@router.post("/generate", response_model=GenerateStoryResponse)
def generate_story_route(payload: GenerateStoryRequest):
    title,text = StoryGenerator().generate_story(payload)
    return GenerateStoryResponse(title=title,text=text)


@router.post("/create")
async def create_story_route(story: StoryCreationRequest):
    creation= await create_story(story.email,story.title,story.paragraph)
    return creation


@router.get("/") 
async def get_stories():
    stories = await db.stories.find().to_list(100)
    return stories

