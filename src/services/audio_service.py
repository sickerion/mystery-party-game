"""Audio generation service using OpenAI TTS."""

import os
from pathlib import Path
from typing import Optional
from openai import OpenAI
from src.config.settings import get_settings


def get_audio_directory() -> Path:
    """Get the audio files directory path."""
    base_dir = Path(__file__).parent.parent.parent
    audio_dir = base_dir / "audio_files"
    audio_dir.mkdir(exist_ok=True)
    return audio_dir


def generate_audio(text: str, game_id: str, audio_type: str, language: str = "en") -> str:
    """
    Generate audio file from text using OpenAI TTS.

    Args:
        text: Text to convert to speech
        game_id: Game ID for filename
        audio_type: Type of audio ('introduction')
        language: Language code ('en' or 'fr')

    Returns:
        Path to the generated audio file (relative to audio_files/)

    Raises:
        Exception: If OpenAI API key is not configured or generation fails
    """
    settings = get_settings()

    if not settings.openai_api_key:
        raise ValueError("OpenAI API key is not configured. Set OPENAI_API_KEY in .env")

    # Initialize OpenAI client
    client = OpenAI(api_key=settings.openai_api_key)

    # Select voice based on language
    # alloy, echo, fable, onyx, nova, shimmer are available voices
    # Use different voices for variety
    voice = "nova" if language == "fr" else "alloy"

    # Create filename
    audio_dir = get_audio_directory()
    filename = f"{game_id}_{audio_type}.mp3"
    filepath = audio_dir / filename

    try:
        # Generate speech using OpenAI TTS
        response = client.audio.speech.create(
            model="tts-1",  # or "tts-1-hd" for higher quality
            voice=voice,
            input=text
        )

        # Save the audio file
        response.stream_to_file(str(filepath))

        # Return relative path (just the filename)
        return filename

    except Exception as e:
        raise Exception(f"Failed to generate audio: {str(e)}")


def delete_audio_files(game_id: str) -> None:
    """
    Delete all audio files for a specific game.

    Args:
        game_id: Game ID
    """
    audio_dir = get_audio_directory()

    # Delete introduction audio
    intro_file = audio_dir / f"{game_id}_introduction.mp3"
    if intro_file.exists():
        intro_file.unlink()


def get_audio_file_path(game_id: str, audio_type: str) -> Optional[Path]:
    """
    Get the full path to an audio file.

    Args:
        game_id: Game ID
        audio_type: Type of audio ('introduction')

    Returns:
        Full path to the audio file if it exists, None otherwise
    """
    audio_dir = get_audio_directory()
    filename = f"{game_id}_{audio_type}.mp3"
    filepath = audio_dir / filename

    return filepath if filepath.exists() else None
