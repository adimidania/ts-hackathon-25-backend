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

    def generate_story(self, request: GenerateStoryRequest) -> tuple[str, str]:
        """Generate a story based on the request and return (title, text).
        Falls back to local formatting if API key missing."""
        tpl = load_prompt("story_generation_prompt.md") or "Story Goal: {story_goal}\nChild: {child_information_name}\nTheme: {story_theme}\nTags: {tags}"
        child = request.child_information
        flat = {
            "story_goal": request.story_goal,
            "tags": ", ".join(request.tags or []),
            "story_length": request.story_length,
            "story_theme": request.story_theme,
            "include_islamic_teaching": request.include_islamic_teaching,
            "additional_instructions": request.additional_instructions or "",
            "child_information_name": child.name,
            "child_information_favorite_pet_name": child.favorite_pet_name or "",
            "child_information_friends_names": ", ".join(child.friends_names or []),
            "child_information_age": child.age or "",
            "child_information_gender": child.gender or "",
            "child_information_description": child.description or "",
        }
        formatted_prompt = tpl.format(**flat)

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=formatted_prompt,
            )
            raw = getattr(response, "text", "") or ""
            title, text = self._extract_title_and_story(raw)
            return title, text
        except Exception:
            # Graceful degradation
            return "Untitled", formatted_prompt + "\n\n(Error calling model; returned formatted prompt.)"

    @staticmethod
    def _extract_title_and_story(output: str) -> tuple[str, str]:
        """Parse model output expecting lines starting with 'Title:' and 'Story:'"""
        title = "Untitled"
        text = output.strip()
        for line in output.splitlines():
            if line.strip().lower().startswith("title:"):
                title = line.split(":", 1)[1].strip()
            if line.strip().lower().startswith("story:"):
                text = line.split(":", 1)[1].strip()
                # Keep the rest after 'Story:' as text
                rest_index = output.lower().find("story:")
                if rest_index != -1:
                    text = output[rest_index + len("Story:"):].strip()
                break
        return title, text