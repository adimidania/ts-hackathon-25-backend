from fastapi import APIRouter

from app.models.requests import GenerateStoryRequest, GenerateStoryResponse
from app.services.text_generation import generate_story

router = APIRouter()


@router.post("/generate", response_model=GenerateStoryResponse)
def generate_story_route(payload: GenerateStoryRequest):
    text = generate_story(prompt_vars=payload.prompt_vars)
    return GenerateStoryResponse(text=text)
