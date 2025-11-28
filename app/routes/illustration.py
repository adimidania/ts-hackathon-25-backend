from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import base64
import io
import zipfile
from fastapi.responses import StreamingResponse

from app.services.story_illustrator import StoryIllustrator

router = APIRouter()


class IllustrateRequest(BaseModel):
    text: str


class IllustrateResponse(BaseModel):
    images: List[str]  # base64 data URIs (e.g., "data:image/png;base64,...")


@router.post("/generate", response_model=IllustrateResponse)
def illustrate_story_route(payload: IllustrateRequest, output: str = "zip"):
    """Generate multiple scene images from full story text.
    - When `output=base64`: returns base64 data URIs in JSON.
    - When `output=zip` (default): returns a single ZIP file containing images.
    No files are saved to storage.
    """
    try:
        illustrator = StoryIllustrator()
        images_bytes = illustrator.generate_images_to_bytes(payload.text)

        if output == "base64":
            data_uris = [
                "data:image/png;base64," + base64.b64encode(b).decode("ascii")
                for b in images_bytes
            ]
            return IllustrateResponse(images=data_uris)

        # Default: package images into an in-memory ZIP and return raw bytes
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for idx, b in enumerate(images_bytes):
                zf.writestr(f"scene_{idx}.png", b)
        buf.seek(0)

        headers = {"Content-Disposition": "inline; filename=story_images.zip"}
        return StreamingResponse(buf, media_type="application/zip", headers=headers)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate images: {e}")
