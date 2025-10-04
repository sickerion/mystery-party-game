"""Image generation service using OpenAI DALL-E."""

import os
import requests
from pathlib import Path
from typing import Optional
from openai import OpenAI
from anthropic import Anthropic
from src.config.settings import get_settings


def get_images_directory() -> Path:
    """Get the images directory path."""
    base_dir = Path(__file__).parent.parent.parent
    images_dir = base_dir / "images"
    images_dir.mkdir(exist_ok=True)
    return images_dir


def sanitize_prompt_with_ai(theme: str, setting: str, language: str) -> str:
    """
    Use Claude AI to sanitize theme and setting, removing sensitive words
    while keeping the essence for image generation.

    Args:
        theme: Original theme text
        setting: Original setting text
        language: Language code

    Returns:
        Sanitized description suitable for DALL-E
    """
    settings = get_settings()
    client = Anthropic(api_key=settings.anthropic_api_key)

    if language == "fr":
        system_prompt = """Tu es un assistant qui transforme des descriptions de jeux de mystère en prompts sûrs pour la génération d'images.

Remplace tous les mots sensibles (meurtre, crime, victime, mort, violence, sang, arme, etc.) par des alternatives neutres et artistiques.
Garde l'ambiance mystérieuse et le contexte visuel, mais rends le tout approprié pour un générateur d'images.

Réponds UNIQUEMENT avec la description transformée, sans explication."""

        user_prompt = f"""Transforme cette description en un prompt sûr pour générer une image:
Thème: {theme}
Décor: {setting}

Crée une description courte (max 2 phrases) qui capture l'ambiance et le décor sans mots sensibles."""
    else:
        system_prompt = """You are an assistant that transforms mystery game descriptions into safe prompts for image generation.

Replace all sensitive words (murder, crime, victim, death, violence, blood, weapon, etc.) with neutral and artistic alternatives.
Keep the mysterious atmosphere and visual context, but make it appropriate for an image generator.

Reply ONLY with the transformed description, no explanation."""

        user_prompt = f"""Transform this description into a safe prompt for image generation:
Theme: {theme}
Setting: {setting}

Create a short description (max 2 sentences) that captures the atmosphere and setting without sensitive words."""

    try:
        message = client.messages.create(
            model=settings.llm_model,
            max_tokens=200,
            temperature=0.7,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )

        sanitized = message.content[0].text.strip()
        return sanitized
    except Exception as e:
        # Fallback to generic prompt if AI sanitization fails
        if language == "fr":
            return "Une scène mystérieuse et élégante avec une ambiance de suspense"
        else:
            return "A mysterious and elegant scene with an atmosphere of suspense"


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

    # Use Claude AI to sanitize the prompt, removing sensitive words
    sanitized_description = sanitize_prompt_with_ai(theme, setting, language)

    # Create final DALL-E prompt with sanitized content
    if language == "fr":
        prompt = f"Une illustration atmosphérique pour un jeu de mystère. {sanitized_description}. Style: élégant, mystérieux, film noir. Pas de texte."
    else:
        prompt = f"An atmospheric illustration for a mystery game. {sanitized_description}. Style: elegant, mysterious, film noir. No text."

    # Create filename
    images_dir = get_images_directory()
    filename = f"{game_id}_cover.png"
    filepath = images_dir / filename

    try:
        # Generate image using DALL-E 3 (higher quality, supports 1024x1024)
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
