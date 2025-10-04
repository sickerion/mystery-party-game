"""Metadata generation node."""

import json
from langchain_core.messages import SystemMessage, HumanMessage
from src.models.state import MysteryGenerationState
from src.graph.nodes.utils import get_llm


def generate_metadata_node(state: MysteryGenerationState) -> MysteryGenerationState:
    """Generate title, instructions, and introduction."""
    llm = get_llm()

    language = state.get('language', 'en')

    if language == 'fr':
        system_prompt = """Tu es un expert concepteur de jeux qui crée des jeux de soirée meurtre et mystère captivants.
Crée des titres accrocheurs, des instructions claires et des introductions atmosphériques."""
    else:
        system_prompt = """You are an expert game designer creating engaging mystery party games.
Create compelling titles, clear instructions, and atmospheric introductions."""

    if language == 'fr':
        user_prompt = f"""Crée les métadonnées pour un jeu de soirée meurtre et mystère:
- Thème: {state['theme']}
- Nombre de joueurs: {state['num_players']}

Fournis:
- title: Titre accrocheur pour le jeu
- estimated_duration: Durée estimée du jeu en minutes
- game_instructions: Instructions claires pour l'hôte du jeu (2-3 paragraphes)
- introduction: Scène d'ouverture atmosphérique pour planter le décor (2-3 paragraphes)

IMPORTANT: Retourne UNIQUEMENT un objet JSON valide. Échappe correctement tous les guillemets et caractères spéciaux dans les chaînes.
Utilise \\n pour les sauts de ligne dans les textes."""
    else:
        user_prompt = f"""Create metadata for a mystery party game:
- Theme: {state['theme']}
- Number of players: {state['num_players']}

Provide:
- title: Catchy title for the game
- estimated_duration: Estimated play time in minutes
- game_instructions: Clear instructions for the game host (2-3 paragraphs)
- introduction: Atmospheric opening scene to set the stage (2-3 paragraphs)

IMPORTANT: Return ONLY valid JSON object. Properly escape all quotes and special characters in strings.
Use \\n for line breaks in text."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    response = llm.invoke(messages)

    # Parse the response and extract metadata
    try:
        content = response.content

        # Try to extract JSON from markdown code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        # Remove any leading/trailing whitespace
        content = content.strip()

        # Try to parse JSON
        try:
            metadata = json.loads(content)
        except json.JSONDecodeError as e:
            # If JSON parsing fails, try to use json.loads with strict=False
            # or try to extract using regex as fallback
            print(f"First JSON parse attempt failed: {e}")
            print(f"Attempting to extract JSON fields manually...")

            # Try to extract fields using basic parsing
            import re

            # Extract title
            title_match = re.search(r'"title"\s*:\s*"([^"]*(?:\\"[^"]*)*)"', content)
            duration_match = re.search(r'"estimated_duration"\s*:\s*(\d+)', content)
            instructions_match = re.search(r'"game_instructions"\s*:\s*"([^"]*(?:\\"[^"]*)*)"', content, re.DOTALL)
            introduction_match = re.search(r'"introduction"\s*:\s*"([^"]*(?:\\"[^"]*)*)"', content, re.DOTALL)

            if not all([title_match, duration_match, instructions_match, introduction_match]):
                # Last resort: Ask LLM to regenerate with simpler prompt
                print("Manual extraction failed, using fallback values")
                raise e

            metadata = {
                "title": title_match.group(1).replace('\\"', '"') if title_match else "Mystery Game",
                "estimated_duration": int(duration_match.group(1)) if duration_match else 120,
                "game_instructions": instructions_match.group(1).replace('\\"', '"') if instructions_match else "Follow the clues",
                "introduction": introduction_match.group(1).replace('\\"', '"') if introduction_match else "A mystery awaits..."
            }

        state["title"] = metadata.get("title")
        state["estimated_duration"] = metadata.get("estimated_duration")
        state["game_instructions"] = metadata.get("game_instructions")
        state["introduction"] = metadata.get("introduction")

    except json.JSONDecodeError as e:
        print(f"Error parsing metadata: {e}")
        print(f"Response content length: {len(response.content)}")
        print(f"Response content (last 1000 chars): {response.content[-1000:]}")
        # Set fallback values
        state["title"] = f"Mystery: {state['theme']}"
        state["estimated_duration"] = 120
        if language == 'fr':
            state["game_instructions"] = "Distribuez les cartes de personnages. Chaque joueur doit lire son rôle en secret. Ensuite, commencez l'enquête."
            state["introduction"] = f"Bienvenue dans ce mystère intrigant sur le thème: {state['theme']}. Un crime a été commis et vous devez découvrir qui est le coupable."
        else:
            state["game_instructions"] = "Distribute character cards. Each player should read their role secretly. Then begin the investigation."
            state["introduction"] = f"Welcome to this intriguing mystery themed: {state['theme']}. A crime has been committed and you must discover who the culprit is."
    except Exception as e:
        print(f"Unexpected error parsing metadata: {e}")
        print(f"Response content: {response.content[:1000]}")

    return state
