from fastapi import FastAPI
from app.routes.story import router as story_router
from app.routes.narration import router as narration_router

app = FastAPI(title="TS Hackathon Backend", version="0.1.0")


@app.get("/")
def read_root():
	return {"status": "ok", "service": "ts-hackathon-backend"}

app.include_router(story_router, prefix="/story", tags=["story-generation"])
app.include_router(narration_router, prefix="/narration", tags=["story-narration"])