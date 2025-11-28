from fastapi import APIRouter

from app.models.requests import GenerateImageRequest, GenerateImageResponse
from ..utils.db_setup import db
router = APIRouter()

