from fastapi import APIRouter

from app.models.requests import GenerateStoryRequest, GenerateStoryResponse
from app.services.text_generation import generate_story

from ..models.story import Story

from ..utils.db_setup import db

router = APIRouter()


@router.post("/generate", response_model=GenerateStoryResponse)
def generate_story_route(payload: GenerateStoryRequest):
    text = generate_story(prompt_vars=payload.prompt_vars)
    return GenerateStoryResponse(text=text)


@router.post("/create")
async def create_story(story: Story):
    res = await db.stories.insert_one(story.dict())
    return {"id": str(res.inserted_id)}

@router.get("/") 
async def get_stories():
    stories = await db.stories.find().to_list(100)
    return stories

