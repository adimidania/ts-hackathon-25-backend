from elevenlabs.client import ElevenLabs
from elevenlabs import play

client = ElevenLabs(
    api_key="sk_b263e4d35f2770d6c938f558dbd8acd26e09197676ccaca6"
)

audio = client.text_to_speech.convert(
    text="The first move is what sets everything in motion.",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)

# Save to a         file
with open("story.mp3", "wb") as f:
    f.write(audio)
     
print("Saved audio to story.mp3. You can play it with any media player.")