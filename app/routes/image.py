from fastapi import APIRouter

from app.models.requests import GenerateImageRequest, GenerateImageResponse
from app.services.image_generation import generate_image
from ..utils.db_setup import db
router = APIRouter()


@router.post("/generate", response_model=GenerateImageResponse)
def generate_image_route(payload: GenerateImageRequest):
    url = generate_image(payload.prompt)
    return GenerateImageResponse(image_url=url)

from fastapi import UploadFile, File, APIRouter
router = APIRouter(prefix="/media")

@router.post("/image")
async def upload_image(file: UploadFile = File(...)):
    path = f"uploads/images/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    res = await db.images.insert_one({"path": path})
    return {"id": str(res.inserted_id), "path": path}
