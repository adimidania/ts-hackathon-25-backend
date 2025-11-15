# TS Hackathon Backend

Minimal FastAPI backend scaffold.

## Setup (Windows PowerShell)

```powershell
# 1. Create virtual environment
python -m venv .venv

# 2. Activate it
.\.venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Environment variables
# Copy .env.example to .env and edit
copy .env.example .env

# Or set temporary variable for current session:
$env:GOOGLE_GEMINI_API_KEY = "your_key_here"

# 5. Run server
uvicorn app.main:app --reload --port 8000
```

Visit: http://127.0.0.1:8000/docs

## Environment File
Edit `.env` (copied from `.env.example`):
```
GOOGLE_GEMINI_API_KEY=your_key_here
```