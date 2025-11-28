![alt text](image.png)

This backend is a FastAPI API that generates kids’ stories, illustrates scenes as images, and narrates audio on-the-fly. It exposes simple REST endpoints for:
- Creating and listing stories
- Generating scene illustrations (ZIP or base64)
- Streaming narration audio (MP3)
- Managing parent accounts and their stories/drafts

Built with FastAPI, Pydantic, and async MongoDB access patterns.

## Tech Stack
- FastAPI for HTTP APIs
- Pydantic for request/response models
- Async DB access via `app.utils.db_setup`
- Python 3.10+ recommended

## Project Structure
- `app/main.py`: FastAPI app setup and router mounting
- `app/routes/`: HTTP endpoints
	- `parent.py`: Register/login, CRUD, and story/draft access for parents
	- `story.py`: Generate text, create stories, list stories
	- `illustrator.py`: Generate scene images (ZIP or base64)
	- `narration.py`: Generate and stream narration MP3
	- `image.py`: Image-related routes (if used)
- `app/services/`: Core logic for generation and handlers
- `app/models/`: Pydantic models and DB schemas
- `app/prompts/`: LLM prompts for story and illustration generation
- `app/utils/`: Auth, DB setup, prompt loader, seed utilities
- `storage/`: Static storage mounted at `/storage`
- `tests/`: Unit tests for generator, illustrator, narrator

## Setup
1. Ensure Python is installed (`python --version`).
2. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

4. Configure environment variables if required (DB connection, API keys). Common examples:
- `MONGODB_URI` or similar in `app/utils/db_setup.py`
- Image/Narration providers keys if used in services

Add them to your shell session or a `.env` loader if implemented.

## Run
Start the FastAPI server with Uvicorn:

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Root health check:
- GET `BASE_URL/` → `{ "status": "ok", "service": "ts-hackathon-backend" }`

Interactive docs:
- Swagger UI: `BASE_URL/docs`
- ReDoc: `BASE_URL/redoc`



### Parent (`/parent`)
- `POST /parent/register` → Register a parent
	- Body: `{ email, full_name, phone_number, password }`
- `POST /parent/login` → Login
	- Body: `{ email, password }`
- `GET /parent/{email}/stories` → List parent’s stories
- `GET /parent/{email}/drafts` → List parent’s drafts
- `GET /parent/` → List all parents
- `GET /parent/{email}` → Get parent
- `DELETE /parent/{email}` → Delete parent
- `PUT /parent/{email}` → Update parent (body: `Parent` model)

### Story (`/story`)
- `POST /story/generate` → Generate a story
	- Body: `GenerateStoryRequest` (see models)
	- Response: `{ title, text }`
- `POST /story/create` → Persist a story
	- Body: `{ email, title, paragraph }`
	- Response: `{ storyId }`
- `GET /story/` → List stories (first 100)

### Illustration (`/illustration`)
- `POST /illustration/generate` → Generate scene images
	- Body: `{ text, max_scenes?, output? }` (`output`: `zip`|`base64`, default `zip`)
	- Response:
		- `zip`: application/zip download `story_images.zip`
		- `base64`: `{ images: ["data:image/png;base64,..."] }`

### Narration (`/narration`)
- `POST /narration/generate` → Stream MP3 for provided title/text
- `GET  /narration/stream?title=...&text=...` → Stream MP3

## Quick Usage Examples

Generate a story:
```powershell
curl -X POST "http://localhost:8000/story/generate" \
	-H "Content-Type: application/json" \
	-d '{
		"age": 7,
		"theme": "adventure",
		"keywords": ["forest","friendly dragon"],
		"language": "en"
	}'
```

Illustrate scenes (ZIP):
```powershell
curl -X POST "http://localhost:8000/illustration/generate" \
	-H "Content-Type: application/json" \
	-d '{
		"text": "Chapter 1...",
		"output": "zip"
	}' --output story_images.zip
```

Narrate audio:
```powershell
curl -X POST "http://localhost:8000/narration/generate" \
	-H "Content-Type: application/json" \
	-d '{
		"title": "A Brave Day",
		"text": "Once upon a time..."
	}' --output narration.mp3
```


## Development Notes
- Prompts live in `app/prompts/` and can be tuned.
- DB setup in `app/utils/db_setup.py`; ensure your connection string.
- Static files available under `/storage`.

## Contributing
- Fork and create a feature branch
- Keep changes minimal and focused
- Add tests for new functionality when feasible
- Open a PR with a clear description

## License
This repository’s license is defined by the project owner. If unspecified, please consult the maintainers before redistribution.

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


## Environment File
Edit `.env` (copied from `.env.example`):
```
GEMINI_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here
MONGO_URI=DATABASE_URI_HERE
```
