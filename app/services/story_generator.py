import os
from google import genai
from dotenv import load_dotenv
from app.models.requests import GenerateStoryRequest
from app.utils.prompt_loader import load_prompt

load_dotenv()

class StoryGenerator:
    def __init__(self, model: str = "gemini-2.5-flash"):
        self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        self.model = model

    def generate_story(self, prompt_vars: GenerateStoryRequest) -> str:
        """Generate a story based on the given prompt.

        Flattens nested child_information for Python .format compatibility.
        """
        prompt = load_prompt("story_generation_prompt.md")
        data = prompt_vars.dict()
        child = data.get("child_information", {}) or {}
        # Normalize dot placeholders to underscore variants used in flat keys
        placeholder_map = {
            "{child_information.name}": "{child_information_name}",
            "{child_information.favorite_pet_name}": "{child_information_favorite_pet_name}",
            "{child_information.friends_names}": "{child_information_friends_names}",
            "{child_information.age}": "{child_information_age}",
            "{child_information.gender}": "{child_information_gender}",
            "{child_information.description}": "{child_information_description}",
        }
        for k, v in placeholder_map.items():
            if k in prompt:
                prompt = prompt.replace(k, v)

        flat = {
            "story_goal": data.get("story_goal", ""),
            "tags": ", ".join(data.get("tags") or []),
            "story_length": data.get("story_length", ""),
            "story_theme": data.get("story_theme", ""),
            "include_islamic_teaching": data.get("include_islamic_teaching", False),
            "additional_instructions": data.get("additional_instructions", ""),
            # child_information_* normalized keys
            "child_information_name": child.get("name", ""),
            "child_information_favorite_pet_name": child.get("favorite_pet_name", ""),
            "child_information_friends_names": ", ".join(child.get("friends_names") or []),
            "child_information_age": child.get("age", ""),
            "child_information_gender": child.get("gender", ""),
            "child_information_description": child.get("description", ""),
            # Back-compat fields used in prompt: references
            "references": data.get("references", ""),
            # Provide a summarized child_information string for templates using {child_information}
            "child_information": (
                f"name={child.get('name','')}, pet={child.get('favorite_pet_name','')}, "
                f"friends={', '.join(child.get('friends_names') or [])}, age={child.get('age','')}, "
                f"gender={child.get('gender','')}, desc={child.get('description','')}"
            ).strip(),
        }
        prompt = prompt.format(**flat)
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
        return response.text