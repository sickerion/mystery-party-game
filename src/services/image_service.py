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
        # Generate image using DALL-E 2 (faster, supports 512x512)
        response = client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            size="512x512",
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


def sanitize_character_prompt_with_ai(name: str, role: str, personality: str, language: str) -> str:
    """
    Use Claude AI to create a safe character portrait prompt.

    Args:
        name: Character name
        role: Character role
        personality: Character personality
        language: Language code

    Returns:
        Sanitized description suitable for DALL-E portrait generation
    """
    settings = get_settings()
    client = Anthropic(api_key=settings.anthropic_api_key)

    if language == "fr":
        system_prompt = """Tu es un assistant qui crée des descriptions de portraits pour la génération d'images.

Crée une description visuelle d'un portrait de personnage basée sur leur rôle et personnalité.
Focus sur: apparence physique, vêtements, expression faciale, style artistique.
Évite tous les mots sensibles et tout contexte criminel.

Réponds UNIQUEMENT avec la description du portrait, sans explication."""

        user_prompt = f"""Crée une description de portrait pour ce personnage:
Nom: {name}
Rôle: {role}
Personnalité: {personality}

Décris le portrait en 2 phrases maximum, style portrait artistique élégant."""
    else:
        system_prompt = """You are an assistant that creates portrait descriptions for image generation.

Create a visual description of a character portrait based on their role and personality.
Focus on: physical appearance, clothing, facial expression, artistic style.
Avoid all sensitive words and criminal context.

Reply ONLY with the portrait description, no explanation."""

        user_prompt = f"""Create a portrait description for this character:
Name: {name}
Role: {role}
Personality: {personality}

Describe the portrait in 2 sentences maximum, elegant artistic portrait style."""

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
        # Fallback to generic portrait prompt if AI sanitization fails
        if language == "fr":
            return f"Portrait élégant d'une personne dans le style {role}"
        else:
            return f"Elegant portrait of a person in the style of {role}"


def generate_character_portrait(
    game_id: str,
    character_id: int,
    name: str,
    role: str,
    personality: str,
    language: str = "en"
) -> str:
    """
    Generate a character portrait image using DALL-E.

    Args:
        game_id: Game ID
        character_id: Character ID
        name: Character name
        role: Character role
        personality: Character personality
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

    # Use Claude AI to sanitize the prompt, creating a safe portrait description
    sanitized_description = sanitize_character_prompt_with_ai(name, role, personality, language)

    # Create final DALL-E prompt with sanitized content
    if language == "fr":
        prompt = f"Portrait de personnage pour jeu de mystère. {sanitized_description}. Style: portrait artistique, élégant, cinématographique. Cadrage: tête et épaules. Pas de texte."
    else:
        prompt = f"Character portrait for mystery game. {sanitized_description}. Style: artistic portrait, elegant, cinematic. Framing: head and shoulders. No text."

    # Create filename - sanitize character name for filesystem
    safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_name = safe_name.replace(' ', '_')
    images_dir = get_images_directory()
    filename = f"{game_id}_character_{character_id}_{safe_name}.png"
    filepath = images_dir / filename

    try:
        # Generate image using DALL-E 2 (512x512)
        response = client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            size="512x512",
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
        raise Exception(f"Failed to generate character portrait: {str(e)}")


def delete_character_image(game_id: str, character_id: int, character_name: str) -> None:
    """
    Delete the portrait image for a specific character.

    Args:
        game_id: Game ID
        character_id: Character ID
        character_name: Character name
    """
    images_dir = get_images_directory()
    safe_name = "".join(c for c in character_name if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_name = safe_name.replace(' ', '_')
    image_file = images_dir / f"{game_id}_character_{character_id}_{safe_name}.png"
    if image_file.exists():
        image_file.unlink()


def get_character_image_file_path(game_id: str, character_id: int, character_name: str) -> Optional[Path]:
    """
    Get the full path to a character portrait image.

    Args:
        game_id: Game ID
        character_id: Character ID
        character_name: Character name

    Returns:
        Full path to the image file if it exists, None otherwise
    """
    images_dir = get_images_directory()
    safe_name = "".join(c for c in character_name if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_name = safe_name.replace(' ', '_')
    filepath = images_dir / f"{game_id}_character_{character_id}_{safe_name}.png"

    return filepath if filepath.exists() else None
