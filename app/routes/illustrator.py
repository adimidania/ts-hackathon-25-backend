from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import io
import zipfile

from app.services.story_illustrator import StoryIllustrator

router = APIRouter()

class IllustrateRequest(BaseModel):
    text: str
    max_scenes: int | None = None
    output: str = "zip"  # zip | base64


@router.post("/generate")
def illustrate_story_route(payload: IllustrateRequest):
    """Generate scene images.
    - Chaining keeps visual continuity (previous image fed into next).
    - Limit scenes via max_scenes.
    - Output options: zip (default) or base64 array.
    """
    try:
        illustrator = StoryIllustrator()
        images_bytes = illustrator.generate_images_to_bytes(
            payload.text
        )

        if not images_bytes:
            raise HTTPException(status_code=400, detail="No images were generated.")

        if payload.output == "base64":
            import base64
            return {
                "images": [
                    "data:image/png;base64," + base64.b64encode(b).decode("ascii")
                    for b in images_bytes
                ]
            }

        # Default ZIP packaging
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for idx, b in enumerate(images_bytes):
                zf.writestr(f"scene_{idx}.png", b)
        buf.seek(0)
        headers = {"Content-Disposition": "attachment; filename=story_images.zip"}
        return StreamingResponse(buf, media_type="application/zip", headers=headers)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate images: {e}")