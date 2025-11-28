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
        """Split text into scenes based on double newlines."""
        paragraphs = story_text.strip().split("\n\n")
        return [p.replace("\n", " ").strip() for p in paragraphs if p.strip()]

    def generate_images_to_bytes(self, story_text: str) -> list[bytes]:
        """
        Generate images for each scene.
        Scene N gets scene N-1 as an input image, so all images look related.
        """
        if not self.client:
            raise RuntimeError("Gemini client not initialized")

        scene_prompts = self.split_story_into_scenes(story_text)
        out: list[bytes] = []

        for idx, scene_text in enumerate(scene_prompts):

            prompt_template = load_prompt("scene_illustration_prompt.md") or "{scene_text}"
            prompt = prompt_template.replace("{scene_text}", scene_text)

            # Build parts (prompt + previous scene image if exists)
            parts = [types.Part.from_text(text=prompt)]

            # If this is NOT the first scene => attach previous scene image
            if idx > 0:
                prev_img_bytes = out[-1]
                parts.append(
                    types.Part.from_bytes(
                        data=prev_img_bytes,
                        mime_type="image/png"
                    )
                )

            contents = [types.Content(role="user", parts=parts)]
            generate_config = types.GenerateContentConfig(response_modalities=["IMAGE"])

            # Read streaming output
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