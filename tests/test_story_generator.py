import pathlib
import sys

# Ensure project root on path when running directly
ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import app.services.story_generator as story_generator_module
from app.services.story_generator import StoryGenerator
from app.models.requests import GenerateStoryRequest, ChildInformation


def test_generate_story_with_full_request():

    req = GenerateStoryRequest(
        child_information=ChildInformation(
            name="Amina",
            favorite_pet_name="Mishmish",
            friends_names=["Layla", "Omar"],
            age=8,
            gender="female",
            description="Curious and kind."
        ),
        story_goal="Teach kindness and patience",
        tags=["friendship", "family"],
        story_length="short",
        story_theme="adventure",
        include_islamic_teaching=True,
        additional_instructions="Keep language simple."
    )

    gen = StoryGenerator()
    result = gen.generate_story(req)
    return result


if __name__ == "__main__":
    print(test_generate_story_with_full_request())
    print("test_generate_story_with_full_request passed")