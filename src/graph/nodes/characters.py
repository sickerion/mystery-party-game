"""Character generation node."""

import json
from langchain_core.messages import SystemMessage, HumanMessage
from src.models.state import MysteryGenerationState
from src.models.schema import Character
from src.graph.nodes.utils import get_llm


def generate_characters_node(state: MysteryGenerationState) -> MysteryGenerationState:
    """Generate characters for the mystery game."""
    llm = get_llm()

    language = state.get('language', 'en')

    if language == 'fr':
        system_prompt = """Tu es un expert écrivain de mystères qui crée des personnages pour un jeu de soirée enquête policière.
Génère des personnages diversifiés et intéressants avec des personnalités, des antécédents et des secrets distincts.
Chaque personnage doit avoir un lien plausible avec le mystère."""
    else:
        system_prompt = """You are an expert mystery writer creating characters for a murder mystery party game.
Generate diverse, interesting characters with distinct personalities, backgrounds, and secrets.
Each character should have a plausible connection to the mystery."""

    if language == 'fr':
        user_prompt = f"""Crée {state['num_players']} personnages VIVANTS jouables pour un jeu de soirée mystère avec les paramètres suivants:
- Thème: {state['theme']}
- Difficulté: {state['difficulty']}
{f"- Demandes spéciales: {state['special_requests']}" if state.get('special_requests') else ""}

IMPORTANT: Ce sont les personnages JOUABLES qui vont enquêter sur le meurtre. Ils sont tous VIVANTS au début du jeu.
La victime sera un PNJ (personnage non-joueur) séparé défini plus tard dans l'intrigue.

Pour chaque personnage VIVANT, fournis:
- name: Nom complet
- role: Leur occupation ou rôle
- background: Bref historique (2-3 phrases, reste concis)
- personality: Traits de personnalité clés (une phrase)
- secret: Un secret caché qu'ils gardent (une phrase)
- motive: Un motif potentiel de meurtre (une phrase, au moins un personnage doit être le futur coupable)
- relationship_to_victim: Comment ils connaissent la victime (sera défini dans l'intrigue, une phrase)

Retourne UNIQUEMENT un tableau JSON valide d'objets personnages, rien d'autre. Garde les descriptions concises pour assurer que le JSON soit complet.
Format d'exemple:
[
  {{
    "name": "Jean Dupont",
    "role": "Détective",
    "background": "Un détective vétéran...",
    "personality": "Cynique mais juste...",
    "secret": "A une dette de jeu...",
    "motive": "La victime connaissait son secret...",
    "relationship_to_victim": "Ancien partenaire..."
  }}
]"""
    else:
        user_prompt = f"""Create {state['num_players']} LIVING player characters for a mystery party game with the following parameters:
- Theme: {state['theme']}
- Difficulty: {state['difficulty']}
{f"- Special requests: {state['special_requests']}" if state.get('special_requests') else ""}

IMPORTANT: These are the PLAYABLE characters who will investigate the murder. They are all ALIVE at the start of the game.
The victim will be a separate NPC (non-player character) defined later in the plot.

For each LIVING character, provide:
- name: Full name
- role: Their occupation or role
- background: Brief background story (2-3 sentences, keep concise)
- personality: Key personality traits (one sentence)
- secret: A hidden secret they're keeping (one sentence)
- motive: A potential motive for murder (one sentence, at least one character should be the future culprit)
- relationship_to_victim: How they know the victim (will be defined in the plot, one sentence)

Return ONLY a valid JSON array of character objects, nothing else. Keep descriptions concise to ensure the JSON is complete.
Example format:
[
  {{
    "name": "John Smith",
    "role": "Detective",
    "background": "A veteran detective...",
    "personality": "Cynical but fair...",
    "secret": "Has a gambling debt...",
    "motive": "Victim knew his secret...",
    "relationship_to_victim": "Former partner..."
  }}
]"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    response = llm.invoke(messages)

    # Parse the response and create Character objects
    try:
        content = response.content

        # Try to extract JSON from markdown code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        # Remove any leading/trailing whitespace
        content = content.strip()

        # Parse JSON
        characters_data = json.loads(content)

        # Handle both array and object with "characters" key
        if isinstance(characters_data, dict) and "characters" in characters_data:
            characters_data = characters_data["characters"]

        characters = [Character(**char) for char in characters_data]
        state["characters"] = characters
    except json.JSONDecodeError as e:
        print(f"Error parsing characters: {e}")
        print(f"Response content length: {len(response.content)}")
        print(f"Response content (last 1000 chars): {response.content[-1000:]}")

        # Try to salvage partial JSON by finding the last complete object
        try:
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            # Try to find the last valid closing bracket
            last_bracket = content.rfind(']')
            if last_bracket > 0:
                # Try parsing up to the last bracket
                truncated_content = content[:last_bracket + 1]
                characters_data = json.loads(truncated_content)

                if isinstance(characters_data, dict) and "characters" in characters_data:
                    characters_data = characters_data["characters"]

                characters = [Character(**char) for char in characters_data]
                state["characters"] = characters
                print(f"Successfully recovered {len(characters)} characters from partial JSON")
                return state
        except Exception as recovery_error:
            print(f"Recovery attempt failed: {recovery_error}")

        # If all fails, set empty list
        state["characters"] = []
    except Exception as e:
        print(f"Unexpected error parsing characters: {e}")
        print(f"Response content: {response.content[:1000]}")
        state["characters"] = []

    return state
