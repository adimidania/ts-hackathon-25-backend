from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, StreamingResponse, Response
from app.models.requests import NarrationRequest, NarrationResponse
from app.services.story_narrator import StoryNarrator

router = APIRouter()

@router.post("/stream")
def stream_narration(payload: NarrationRequest):
    narrator = StoryNarrator()
    try:
        audio_bytes = narrator.narrate_to_bytes(payload.title, payload.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate narration: {e}")
    filename = f"{payload.title.replace(' ', '_')[:40] or 'story'}.mp3"
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return StreamingResponse(iter([audio_bytes]), media_type="audio/mpeg", headers=headers)