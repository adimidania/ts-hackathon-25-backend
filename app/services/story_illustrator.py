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

    def save_binary_file(self, file_name: str, data: bytes):
        """Save binary data to a file."""
        with open(file_name, "wb") as f:
            f.write(data)
        print(f"File saved to: {file_name}")

    def generate_image(self, prompt: str, input_image_path: str = None, output_prefix: str = "generated_image"):
        """Generate an image from a prompt (optionally using a base image)."""
        parts = [types.Part.from_text(text=prompt)]

        if input_image_path:
            with open(input_image_path, "rb") as f:
                image_bytes = f.read()
            mime_type = mimetypes.guess_type(input_image_path)[0] or "image/png"
            parts.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type))

        contents = [types.Content(role="user", parts=parts)]
        generate_config = types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"])

        file_index = 0
        output_paths = []

        for chunk in self.client.models.generate_content_stream(
            model=self.model,
            contents=contents,
            config=generate_config,
        ):
            if not chunk.candidates or not chunk.candidates[0].content.parts:
                continue

            part = chunk.candidates[0].content.parts[0]
            if part.inline_data and part.inline_data.data:
                file_extension = mimetypes.guess_extension(part.inline_data.mime_type) or ".png"
                output_path = f"{output_prefix}_{file_index}{file_extension}"
                self.save_binary_file(output_path, part.inline_data.data)
                output_paths.append(output_path)
                file_index += 1
            else:
                print(chunk.text)

        return output_paths

    def split_story_into_scenes(self, story_text: str):
        """
        Split the story text into a list of scene prompts.
        This is a placeholder. You can implement NLP logic, simple paragraph splitting,
        or even use a model to detect scenes.
        """
        # Split by double newline (paragraphs)
        paragraphs = story_text.strip().split("\n\n")
        return [p.replace("\n", " ").strip() for p in paragraphs if p.strip()]

    def illustrate_story(self, story_text: str, output_prefix: str = "scene"):
        """Main pipeline: split story and generate images for each scene."""
        scene_prompts = self.split_story_into_scenes(story_text)
        all_images = []

        for idx, scene_text in enumerate(scene_prompts):
            prompt = load_prompt("scene_illustration_prompt.md").replace("{scene_text}", scene_text)
            print(f"Generating image for scene {idx}: {prompt[:50]}...")

            input_image = all_images[idx - 1] if idx > 0 else None

            images = self.generate_image(
                prompt,
                input_image_path=input_image,
                output_prefix=f"{output_prefix}_{idx}"
            )

            all_images.extend(images)

        return all_images
