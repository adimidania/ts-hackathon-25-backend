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
    story = "Amina, a lovely small girl with a twinkle in her eye, was at home with her dearest friend, Leila. Her fluffy pet, named 'pet', was napping by her feet. It was a lazy afternoon, and Amina and Leila were getting a bit bored. \"Let's make something amazing!\" whispered Amina. \"A super-duper surprise cake for Mama!\" Leila’s eyes lit up. This sounded like a grand adventure!\n\nThey tiptoed into the kitchen, quiet as mice. \"First, the flour!\" Amina announced. Being lovely small, Amina needed to climb onto a wobbly stool to reach the big bag of flour on the top shelf. She stretched, her tiny fingers just grasping the handle. \"Got it!\" she cheered, giving it a mighty tug. But the bag was heavier than it looked! *WHOOSH!* The bag tilted, then tumbled, releasing a giant, fluffy cloud of white flour all over the kitchen!\n\nAmina and Leila stood frozen, looking like two little snowmen in the middle of a blizzard. Even 'pet', startled awake, was covered in a powdery white mustache! Amina giggled, then gasped. \"Oh no! Mama is going to see!\" They looked at the white floor, the white counter, the white chairs, and each other, covered head to toe in white. \"Let's clean it really fast!\" whispered Leila, but their quick attempts only spread the flour further, making it look like a very silly, very messy snow angel had visited their kitchen.\n\nAmina's tummy started to feel a little wobbly, not from the flour, but from worry. She knew she should tell Mama, but it was so messy! What if Mama was upset? Then, she remembered Mama’s gentle voice, explaining the beautiful words from the Quran: \"O you who have believed, fear Allah and be with those who are truthful.\" (Quran 9:119). Mama had taught her that this means Allah loves people who are brave enough to tell the truth, even if they’re a little scared, because it makes their hearts feel light and happy.\n\nTaking a deep breath, Amina grabbed Leila's hand. They marched out of the kitchen, looking like two little flour ghosts, with 'pet' trotting bravely behind, still sporting his floury whiskers. \"Mama?\" Amina squeaked, trying not to giggle as she saw Mama’s surprised face. \"We... uh... tried to make you a surprise cake, and...\" She pointed back to the kitchen, where a white cloud still seemed to hang in the air.\n\nMama walked to the kitchen, took one look at the hilarious flour-covered scene, and then at her two little snow-children and their snowy 'pet', and burst into laughter! \"Oh, my sweet girls!\" she chuckled, wiping tears from her eyes. \"Thank you for being honest, Amina. Accidents happen, and it’s always best to tell the truth.\" Together, they cleaned up the mess, laughing the whole time. Mama even helped them bake a *real* cake, and it was the most delicious cake ever, made even sweeter by Amina's honest heart."

    # Make sure output folder exists
    output_folder.mkdir(parents=True, exist_ok=True)

    # Run illustration pipeline
    paragraphs = si.split_story_into_scenes(story)

    print(f"Story split into {len(paragraphs)} scenes.")


if __name__ == "__main__":
    # Define a folder to save generated images
    output_dir = pathlib.Path("./storage")
    test_illustrate_story_pipeline(output_dir)