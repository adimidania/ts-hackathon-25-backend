from app.utils.prompt_loader import load_prompt

def generate_story(prompt_vars: dict | None = None) -> str:
    template = load_prompt("story_prompt.txt")
    pass
