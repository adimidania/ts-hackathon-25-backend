from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.story import router as story_router
from app.routes.narration import router as narration_router
from app.routes.illustration import router as illustration_router

app = FastAPI(title="TS Hackathon Backend", version="0.1.0")

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.get("/")
def read_root():
	return {"status": "ok", "service": "ts-hackathon-backend"}

app.include_router(story_router, prefix="/story", tags=["story-generation"])
app.include_router(narration_router, prefix="/narration", tags=["story-narration"])
app.include_router(illustration_router, prefix="/illustration", tags=["story-illustration"])