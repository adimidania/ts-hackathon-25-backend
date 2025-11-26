from fastapi import FastAPI
from app.routes.story import router as story_router

app = FastAPI(title="TS Hackathon Backend", version="0.1.0")


@app.get("/")
def read_root():
	return {"status": "ok", "service": "ts-hackathon-backend"}


app.include_router(story_router, tags=["story-generation"])