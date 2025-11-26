from fastapi import APIRouter

from app.models.requests import GenerateStoryRequest, GenerateStoryResponse
from app.services.story_generator import StoryGenerator

router = APIRouter()

@router.post("/generate", response_model=GenerateStoryResponse)
def generate_story_route(payload: GenerateStoryRequest):
    title, text = StoryGenerator().generate_story(payload)
    return GenerateStoryResponse(title=title, text=text)