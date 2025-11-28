from fastapi import APIRouter

from app.services.stories_handlers import get_stories_images
from app.models.requests import GenerateImageRequest, GenerateImageResponse
from ..utils.db_setup import db
from fastapi import HTTPException
from ..utils.db_setup import obj_id 
router = APIRouter()
