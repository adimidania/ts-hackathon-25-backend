from pathlib import Path


PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"

def load_prompt(name: str) -> str | None:
    path = PROMPTS_DIR / name
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return None
