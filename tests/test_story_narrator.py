import pathlib
import sys
import tempfile

# Ensure project root on path when running directly
ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import re
from app.services.story_narrator import StoryNarrator

def test_narrate_story():
    title = "Amina and the Case of the Missing Sparkle Ball"
    story = "One sunny afternoon, Amina was playing in her cozy living room with her best friends, Layla and Omar. Her fluffy white kitten, Mishmish, was chasing a sparkly ball, a special gift from her grandpa. Mishmish loved that ball more than anything! Amina, curious as ever, watched Mishmish pounce and bat it under the sofa. \"Look!\" she giggled, \"Mishmish thinks she's a tiny lion!\" Layla and Omar laughed too, enjoying the kitten's playful antics.\n\nSuddenly, Mishmish darted behind a big bookshelf and then... poof! The kitten reappeared, but the sparkly ball was gone. Amina frowned. \"Where did it go?\" she wondered, her eyes scanning the area. Mishmish purred, rubbing against Amina's legs as if asking for help. Amina, Layla, and Omar immediately began their search, turning this small mystery into an exciting adventure. They peeked behind cushions, under rugs, and even inside Omar's backpack, but no sparkly ball.\n\nAmina started to feel a little impatient. \"Oh, Mishmish! Why did you hide it so well?\" she sighed, tapping her foot. Layla suggested looking in the kitchen, while Omar wanted to check the bedrooms. They started running around, a bit disorganized. Just then, Amina's mother walked in, smiling kindly. She saw their worried faces and the frantic search. \"What's the matter, my dears?\" she asked softly.\n\nAmina explained about the missing sparkly ball. Her mother nodded, then sat down calmly. \"Sometimes, when things are tricky, we need to remember two important things: kindness and patience,\" she said gently. \"Do you remember the beautiful Hadith about kindness? Our Prophet Muhammad (peace be upon him) taught us, 'Be kind to those on earth and He who is in the heavens will be kind to you.'\" Amina's mother explained that this means when we are kind to everyone, even little Mishmish or to each other when we're frustrated, Allah will be kind to us.\n\nTaking a deep breath, Amina decided to try a different approach. Instead of rushing, she thought carefully about Mishmish's favorite hiding spots. \"Let's be very patient and look slowly, friends,\" she suggested. They gently moved a few books on the bottom shelf, peering into the small gaps. Layla pointed to a tiny opening. \"Amina, look there!\" she whispered.\n\nPeeking inside, Amina saw two bright, sparkly eyes looking back! It wasn't the ball, but Mishmish herself, snuggled up with the sparkly ball nestled right beside her, fast asleep. Amina giggled and carefully reached in to retrieve the ball and the sleepy kitten. They all cheered quietly, happy that their patience and gentle search had paid off. Amina hugged Mishmish, feeling a warmth spread through her heart. She learned that day that with kindness and patience, even the trickiest mysteries can be solved, and it makes every adventure much more joyful."

    narration = StoryNarrator().narrate(title, story)

    print("Narration path:", narration)


if __name__ == "__main__":
    test_narrate_story()
    print("story_narrator tests passed")
