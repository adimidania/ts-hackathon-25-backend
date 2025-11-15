from fastapi import APIRouter

from app.models.requests import GenerateImageRequest, GenerateImageResponse
from app.services.image_generation import generate_image

router = APIRouter()


@router.post("/generate", response_model=GenerateImageResponse)
def generate_image_route(payload: GenerateImageRequest):
    url = generate_image(payload.prompt)
    return GenerateImageResponse(image_url=url)
