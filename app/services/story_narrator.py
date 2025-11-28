import os
import time
import pathlib
import re
from typing import Optional
from dotenv import load_dotenv, find_dotenv
from elevenlabs.client import ElevenLabs


# Load .env robustly regardless of current working directory
load_dotenv(find_dotenv())

class StoryNarrator:
    """Generate narration audio for a story using ElevenLabs.
    """

    def __init__(
        self,
        voice_id: Optional[str] = None,
        model_id: Optional[str] = None,
        output_format: str = "mp3_44100_128",
    ):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        # Allow overriding via env
        self.voice_id = voice_id or os.getenv("ELEVENLABS_VOICE_ID", "tQ4MEZFJOzsahSEEZtHK")
        self.model_id = model_id or os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")
        self.output_format = output_format
        self.output_dir = pathlib.Path("storage/audio")
        self._client = ElevenLabs(api_key=self.api_key) if (self.api_key and ElevenLabs) else None

    def narrate(self, title: str, story_text: str, pause_seconds: float = 1.0) -> str:
        safe_title = "_".join(title.split())[:40] or "story"
        ts = int(time.time())
        base_name = f"{safe_title}_{ts}"
        audio_path = self.output_dir / f"{base_name}.mp3"

        # Build text with simple paragraph separation (avoid SSML tags not supported by ElevenLabs)
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", story_text.strip()) if p.strip()]
        if paragraphs:
            body = ".\n\n".join(paragraphs)
        else:
            body = story_text.strip()
        full_text = f"{title}. {body}".strip()
        try:
            # Ensure output directory exists
            self.output_dir.mkdir(parents=True, exist_ok=True)
            if not self._client:
                raise RuntimeError("ElevenLabs client is not initialized (missing API key or SDK)")
            audio = self._client.text_to_speech.convert(
                text=full_text,
                voice_id=self.voice_id,
                model_id=self.model_id,
                output_format=self.output_format,
            )
            # audio may be bytes or a generator depending on SDK; normalize
            if hasattr(audio, "__iter__") and not isinstance(audio, (bytes, bytearray)):
                data = b"".join(audio) 
            else:
                data = audio 
            if not data:
                raise RuntimeError("Received empty audio data from ElevenLabs")
            with open(audio_path, "wb") as f:
                f.write(data)
            return str(audio_path)
        except Exception as e:
            # Ensure directory exists even on error
            self.output_dir.mkdir(parents=True, exist_ok=True)
            error_file = self.output_dir / f"{base_name}_error.txt"
            error_file.write_text(f"Generation failed: {e}")
            return str(error_file)

    def narrate_to_bytes(self, title: str, story_text: str, pause_seconds: float = 1.0) -> bytes:
        """Generate narration and return raw audio bytes without touching the filesystem."""
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", story_text.strip()) if p.strip()]
        body = ".\n\n".join(paragraphs) if paragraphs else story_text.strip()
        full_text = f"{title}. {body}".strip()

        if not self._client:
            raise RuntimeError("ElevenLabs client is not initialized (missing API key or SDK)")

        audio = self._client.text_to_speech.convert(
            text=full_text,
            voice_id=self.voice_id,
            model_id=self.model_id,
            output_format=self.output_format,
        )
        if hasattr(audio, "__iter__") and not isinstance(audio, (bytes, bytearray)):
            data = b"".join(audio)  # type: ignore
        else:
            data = audio  # type: ignore
        if not data:
            raise RuntimeError("Received empty audio data from ElevenLabs")
        return data

__all__ = ["StoryNarrator"]