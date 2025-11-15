from app.utils.prompt_loader import load_prompt

def generate_image(prompt: str) -> str:
    template = load_prompt("image_generation_prompt.txt")
    pass
