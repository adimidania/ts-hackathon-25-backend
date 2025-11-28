import pathlib
import sys

ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.services.story_illustrator import StoryIllustrator

def test_illustrate_story_pipeline(output_folder: pathlib.Path):
    """
    Run the full illustrate_story pipeline without pytest.
    """
    si = StoryIllustrator()
    story = """
    Amina was sitting quietly in her room, the soft afternoon light streaming through the window. 
    She held her Quran gently in her hands, turning the pages with care. The room was calm, and 
    she felt at peace as she read, her eyes moving slowly over each word. The gentle rustle of the 
    pages and the occasional chirping of birds outside created a perfect moment for reflection.

    As she read, a particular verse caught her attention. Its words seemed to glow with meaning, 
    and she paused to think about them. Slowly, the message of the verse unfolded in her mind, 
    and she felt a deep sense of understanding and joy. It was as if the verse had been written 
    just for her, offering comfort and guidance.

    Filled with excitement, Amina got up and went to the kitchen, where her mother was preparing tea. 
    She told her mother about the verse she had found and explained what it meant to her. Her mother 
    smiled warmly, listening with pride, and they shared a quiet moment together, reflecting on the 
    beauty of the words and the lessons they held.
    """

    # Make sure output folder exists
    output_folder.mkdir(parents=True, exist_ok=True)

    # Run illustration pipeline
    images = si.illustrate_story(story_text=story, output_prefix=str(output_folder / "scene"))

    # Simple assertions
    if len(images) < 2:
        raise Exception("Expected at least one image per scene!")

    for p in images:
        if not pathlib.Path(p).exists():
            raise Exception(f"Generated file does not exist: {p}")

    print("All images generated successfully:", images)


if __name__ == "__main__":
    # Define a folder to save generated images
    output_dir = pathlib.Path("./storage")
    test_illustrate_story_pipeline(output_dir)