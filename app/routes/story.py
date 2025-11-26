from fastapi import APIRouter

from app.models.requests import GenerateStoryRequest, GenerateStoryResponse
from app.services.story_generator import StoryGenerator
from app.services.story_illustrator import StoryIllustrator

router = APIRouter()

@router.post("/generate", response_model=GenerateStoryResponse)
def generate_story_route(payload: GenerateStoryRequest):
    text = StoryGenerator().generate_story(prompt_vars=payload.dict())
    # images = StoryIllustrator().illustrate_story(story_text=text, output_prefix="storage/scene")
    return GenerateStoryResponse(text=text)