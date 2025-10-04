"""Image generation service using OpenAI DALL-E."""

import os
import requests
from pathlib import Path
from typing import Optional
from openai import OpenAI
from src.config.settings import get_settings


def get_images_directory() -> Path:
    """Get the images directory path."""
    base_dir = Path(__file__).parent.parent.parent
    images_dir = base_dir / "images"
    images_dir.mkdir(exist_ok=True)
    return images_dir


def generate_cover_image(game_id: str, theme: str, setting: str, language: str = "en") -> str:
    """
    Generate a cover image for a mystery game using DALL-E.

    Args:
        game_id: Game ID for filename
        theme: Theme of the mystery
        setting: Setting description from the plot
        language: Language code ('en' or 'fr')

    Returns:
        Path to the generated image file (relative to images/)

    Raises:
        Exception: If OpenAI API key is not configured or generation fails
    """
    settings = get_settings()

    if not settings.openai_api_key:
        raise ValueError("OpenAI API key is not configured. Set OPENAI_API_KEY in .env")

    # Initialize OpenAI client
    client = OpenAI(api_key=settings.openai_api_key)

    # Create prompt for DALL-E based on theme and setting
    if language == "fr":
        prompt = f"Une illustration atmosphérique et mystérieuse pour un jeu de soirée meurtre et mystère. Thème: {theme}. Décor: {setting}. Style: élégant, mystérieux, avec une ambiance de film noir. Pas de texte."
    else:
        prompt = f"An atmospheric and mysterious illustration for a murder mystery party game. Theme: {theme}. Setting: {setting}. Style: elegant, mysterious, with a film noir atmosphere. No text."

    # Create filename
    images_dir = get_images_directory()
    filename = f"{game_id}_cover.png"
    filepath = images_dir / filename

    try:
        # Generate image using DALL-E
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        # Get image URL from response
        image_url = response.data[0].url

        # Download and save the image
        image_response = requests.get(image_url)
        image_response.raise_for_status()

        with open(filepath, 'wb') as f:
            f.write(image_response.content)

        # Return relative path (just the filename)
        return filename

    except Exception as e:
        raise Exception(f"Failed to generate image: {str(e)}")


def delete_cover_image(game_id: str) -> None:
    """
    Delete the cover image for a specific game.

    Args:
        game_id: Game ID
    """
    images_dir = get_images_directory()
    image_file = images_dir / f"{game_id}_cover.png"
    if image_file.exists():
        image_file.unlink()


def get_image_file_path(game_id: str) -> Optional[Path]:
    """
    Get the full path to a cover image.

    Args:
        game_id: Game ID

    Returns:
        Full path to the image file if it exists, None otherwise
    """
    images_dir = get_images_directory()
    filepath = images_dir / f"{game_id}_cover.png"

    return filepath if filepath.exists() else None
