from fastapi import FastAPI
from app.routes.story import router as story_router
from app.routes.illustrator import router as illustration_router
from app.routes.image import router as image_router
from app.routes.parent import router as parent_router
from app.routes.narration import router as narration_router
from fastapi.staticfiles import StaticFiles
#from app.routes.Audio import router as audio_router
app = FastAPI(title="TS Hackathon Backend", version="0.1.0")


@app.get("/")
def read_root():
	return {"status": "ok", "service": "ts-hackathon-backend"}




app.include_router(parent_router, prefix="/parent", tags=["parent"])
app.include_router(image_router, prefix="/image", tags=["image"])
app.include_router(narration_router,prefix='/narration',tags=["narration"])
app.include_router(story_router, prefix="/story", tags=["story"])
app.include_router(illustration_router, prefix="/illustration", tags=["story-illustration"])


app.mount("/storage", StaticFiles(directory="storage"), name="storage")