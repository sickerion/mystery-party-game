"""Plot generation node."""

import json
from langchain_core.messages import SystemMessage, HumanMessage
from src.models.state import MysteryGenerationState
from src.models.schema import Plot
from src.graph.nodes.utils import get_llm


def generate_plot_node(state: MysteryGenerationState) -> MysteryGenerationState:
    """Generate the main plot and storyline."""
    llm = get_llm()

    language = state.get('language', 'en')

    characters_summary = "\n".join([
        f"- {char.name} ({char.role}): {char.background}"
        for char in state.get("characters", [])
    ])

    if language == 'fr':
        system_prompt = """Tu es un expert écrivain de mystères qui crée des intrigues captivantes pour des soirées meurtre et mystère.
Crée une intrigue cohérente et engageante qui lie tous les personnages ensemble avec une résolution satisfaisante."""
    else:
        system_prompt = """You are an expert mystery writer creating compelling murder mystery plots.
Create a coherent, engaging plot that ties all characters together with a satisfying resolution."""

    if language == 'fr':
        user_prompt = f"""Crée une intrigue de soirée meurtre et mystère pour un jeu de société avec ces paramètres:
- Thème: {state['theme']}
- Difficulté: {state['difficulty']}

Personnages joueurs vivants (tous suspects/enquêteurs jouables):
{characters_summary}

Fournis un objet JSON avec ces champs exacts:
- setting: STRING - Description du cadre (2 phrases max)
- victim: STRING - Nom de la victime (doit être un PNJ, PAS un des personnages joueurs ci-dessus)
- crime: STRING - Description du crime (1 phrase)
- culprit: STRING - Nom du coupable (DOIT être un des personnages joueurs ci-dessus)
- murder_method: STRING - Comment le crime a été commis (1 phrase)
- timeline: ARRAY de STRINGS - 5-7 événements clés (bref, 1 phrase chacun)
- resolution: STRING - Comment le mystère peut être résolu (2-3 phrases max)

CRITIQUE: Garde TOUTES les descriptions CONCISES (1-3 phrases) pour assurer une réponse JSON complète.
Retourne UNIQUEMENT du JSON valide, rien d'autre.

Format d'exemple:
{{
  "setting": "Un manoir victorien pendant un orage. Les invités sont piégés à l'intérieur.",
  "victim": "Lord Blackwood",
  "crime": "Empoisonné pendant le dîner",
  "culprit": "Lady Smith",
  "murder_method": "Arsenic dans le vin",
  "timeline": ["Les invités arrivent à 18h", "Le dîner est servi à 19h", "La victime s'effondre à 20h"],
  "resolution": "Le verre de vin empoisonné porte des empreintes correspondant au coupable."
}}"""
    else:
        user_prompt = f"""Create a murder mystery plot for a party game with these parameters:
- Theme: {state['theme']}
- Difficulty: {state['difficulty']}

Living player characters (all playable suspects/investigators):
{characters_summary}

Provide a JSON object with these exact fields:
- setting: STRING - Setting description (2 sentences max)
- victim: STRING - Name of the victim (must be an NPC, NOT one of the player characters above)
- crime: STRING - Description of the crime (1 sentence)
- culprit: STRING - Name of the culprit (MUST be one of the player characters above)
- murder_method: STRING - How the crime was committed (1 sentence)
- timeline: ARRAY of STRINGS - 5-7 key events (brief, 1 sentence each)
- resolution: STRING - How the mystery can be solved (2-3 sentences max)

CRITICAL: Keep ALL descriptions CONCISE (1-3 sentences) to ensure complete JSON response.
Return ONLY valid JSON, nothing else.

Example format:
{{
  "setting": "A Victorian mansion during a thunderstorm. Guests are trapped inside.",
  "victim": "Lord Blackwood",
  "crime": "Poisoned during dinner",
  "culprit": "Lady Smith",
  "murder_method": "Arsenic in the wine",
  "timeline": ["Guest arrive at 6pm", "Dinner served at 7pm", "Victim collapses at 8pm"],
  "resolution": "The poisoned wine glass has fingerprints matching the culprit."
}}"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    response = llm.invoke(messages)

    # Parse the response and create Plot object
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
        plot_data = json.loads(content)
        plot = Plot(**plot_data)
        state["plot"] = plot
    except json.JSONDecodeError as e:
        print(f"Error parsing plot: {e}")
        print(f"Response content length: {len(response.content)}")
        print(f"Response content (last 1000 chars): {response.content[-1000:]}")

        # Try to salvage partial JSON by finding the last complete closing brace
        try:
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            # Try to find the last valid closing brace
            last_brace = content.rfind('}')
            if last_brace > 0:
                # Try parsing up to the last brace
                truncated_content = content[:last_brace + 1]
                plot_data = json.loads(truncated_content)
                plot = Plot(**plot_data)
                state["plot"] = plot
                print(f"Successfully recovered plot from partial JSON")
                return state
        except Exception as recovery_error:
            print(f"Recovery attempt failed: {recovery_error}")

        state["plot"] = None
    except Exception as e:
        print(f"Unexpected error parsing plot: {e}")
        print(f"Response content: {response.content[:1000]}")
        state["plot"] = None

    return state
