from fastapi import FastAPI

from app.routes.story import router as story_router
from app.routes.image import router as image_router
from app.routes.parent import router as parent_router
#from app.routes.Audio import router as audio_router
app = FastAPI(title="TS Hackathon Backend", version="0.1.0")


@app.get("/")
def read_root():
	return {"status": "ok", "service": "ts-hackathon-backend"}


app.include_router(story_router, prefix="/story", tags=["story"])
#app.include_router(image_router, prefix="/image", tags=["image"])
#app.include_router(audio_router, prefix="/audio", tags=["audio"])
app.include_router(parent_router, prefix="/parent", tags=["parent"])