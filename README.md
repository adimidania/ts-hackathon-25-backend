# TS Hackathon Backend

FastAPI service that:
1. Generates personalized children's stories (Gemini).
2. Streams spoken narration audio (ElevenLabs).

---
## Quick Setup (Windows PowerShell)
```powershell
# Create & activate virtual env
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install deps
pip install -r requirements.txt

# (Optional) set env var for current session
$env:GOOGLE_GEMINI_API_KEY = "your_key_here"
$env:ELEVENLABS_API_KEY = "your_key_here"

# Run API (default: http://127.0.0.1:8000)
uvicorn app.main:app --reload --port 8000
```
Docs UI: http://127.0.0.1:8000/docs

Run tests:
```powershell
pytest -q
```

---
## Key Endpoints

- `POST /narration/generate` — Generate and stream MP3 from JSON body `{ title, text }`.
- `POST /narration/stream` — Same as above, streams MP3 from JSON body; preferred for long texts.

Example (PowerShell):
```powershell
curl -X POST "http://127.0.0.1:8000/narration/stream" `
	-H "Content-Type: application/json" `
	-d '{
		"title": "Meriem and the Floury Mishmish Adventure",
		"text": "Meriem, with her bright blue eyes..."
	}' --output narration.mp3
```

---
## Minimal .env
```
GOOGLE_GEMINI_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here
```
