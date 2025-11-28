import asyncio
from faker import Faker
from motor.motor_asyncio import AsyncIOMotorClient
import random
from db_setup import db

fake = Faker()

NUM_PARENTS = 10
NUM_STORIES_PER_PARENT = 5
NUM_IMAGES = 20
NUM_AUDIO = 10


async def seed_images():
    images = [{"path": f"/images/{fake.file_name(extension='png')}"} for _ in range(NUM_IMAGES)]
    result = await db.images.insert_many(images)
    return [str(id) for id in result.inserted_ids]


async def seed_audio():
    audio = [{"path": f"/audio/{fake.file_name(extension='mp3')}"} for _ in range(NUM_AUDIO)]
    result = await db.audio.insert_many(audio)
    return [str(id) for id in result.inserted_ids]


async def seed_parents_and_stories(image_ids, audio_ids):
    parent_ids = []

    for _ in range(NUM_PARENTS):

        parent = {
            "email": fake.email(),
            "full_name": fake.name(),
            "phone_number": fake.phone_number(),
            "hashed_password": "test123",  
            "stories": [],
            "drafts": []
        }

        parent_res = await db.parents.insert_one(parent)
        parent_id = str(parent_res.inserted_id)
        parent_ids.append(parent_id)

        for _ in range(NUM_STORIES_PER_PARENT):
            story = {
                "title": fake.sentence(),
                "main_character": fake.first_name(),
                "age": random.randint(4, 12),
                "characters": [fake.first_name() for _ in range(random.randint(1, 4))],
                "gender": random.choice(["Male", "Female"]),
                "picture": random.choice(image_ids),
                "paragraph": fake.text(),
                "pictures": random.sample(image_ids, random.randint(0, 3)),
                "audio": random.choice(audio_ids),
                "values": ["kindness", "honesty", "sharing"],
                "style": random.choice(["funny", "adventure", "moral"]),
                "theme": random.choice(["friendship", "family", "courage"]),
                "islamic_teaching": random.choice(["respect", "truthfulness", "patience"]),
                "description": fake.sentence(),
                "tags": [fake.word() for _ in range(3)],
                "is_draft": random.choice([True, False])
            }

            story_res = await db.stories.insert_one(story)
            story_id = str(story_res.inserted_id)

            if story["is_draft"]:
                await db.parents.update_one(
                    {"_id": parent_res.inserted_id},
                    {"$push": {"drafts": story_id}}
                )
            else:
                await db.parents.update_one(
                    {"_id": parent_res.inserted_id},
                    {"$push": {"stories": story_id}}
                )

    return parent_ids


async def main():
    print(" Seeding images...")
    image_ids = await seed_images()

    print("Seeding audio...")
    audio_ids = await seed_audio()

    print("Seeding parents and stories...")
    await seed_parents_and_stories(image_ids, audio_ids)

    print("Database seeded successfully.")


if __name__ == "__main__":
    asyncio.run(main())
