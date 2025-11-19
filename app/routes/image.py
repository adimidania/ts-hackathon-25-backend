from fastapi import APIRouter

from app.models.requests import GenerateImageRequest, GenerateImageResponse
from app.services.story_illustrator import StoryIllustrator

router = APIRouter()
illustrator = StoryIllustrator()


@router.post("/generate", response_model=GenerateImageResponse)
def generate_image_route(payload: GenerateImageRequest):
    # Use first generated image path or empty string if none.
    images = illustrator.generate_image(prompt=payload.prompt)
    return GenerateImageResponse(image_url=images[0] if images else "")
