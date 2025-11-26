from fastapi import APIRouter

from app.models.requests import GenerateAudioRequest
from app.services.audio_generation import generate_audio
router = APIRouter()

@router.post('/generate', response_model=GenerateAudioRequest)
def generate_audio_route(payload: GenerateAudioRequest):
    audio_url = generate_audio(payload.text)
    return {'audio_url': audio_url}