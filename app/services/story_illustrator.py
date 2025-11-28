import os
import mimetypes
from google import genai
from google.genai import types
from app.utils.prompt_loader import load_prompt
from dotenv import load_dotenv

load_dotenv()

class StoryIllustrator:
    def __init__(self, model: str = "gemini-2.5-flash-image-preview"):
        self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        self.model = model

    def split_story_into_scenes(self, story_text: str):
        """
        Split the story text into a list of scene prompts.
        Simple paragraph splitting by double newline.
        """
        paragraphs = story_text.strip().split("\n\n")
        return [p.replace("\n", " ").strip() for p in paragraphs if p.strip()]

    def generate_images_to_bytes(self, story_text: str) -> list[bytes]:
        """Generate images for each scene and return raw bytes."""
        if not self.client:
            raise RuntimeError("Gemini client not initialized (missing GEMINI_API_KEY)")

        scene_prompts = self.split_story_into_scenes(story_text)
        out: list[bytes] = []

        for idx, scene_text in enumerate(scene_prompts):
            prompt_template = load_prompt("scene_illustration_prompt.md") or "{scene_text}"
            prompt = prompt_template.replace("{scene_text}", scene_text)

            parts = [types.Part.from_text(text=prompt)]
            contents = [types.Content(role="user", parts=parts)]
            generate_config = types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"])

            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=generate_config,
            ):
                for candidate in chunk.candidates or []:
                    for part in candidate.content.parts or []:
                        if getattr(part, "inline_data", None) and part.inline_data.data:
                            out.append(part.inline_data.data)

        return out
