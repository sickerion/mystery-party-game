"""Character generation node."""

import json
from langchain_core.messages import SystemMessage, HumanMessage
from src.models.state import MysteryGenerationState
from src.models.schema import Character
from src.graph.nodes.utils import get_llm


def generate_characters_node(state: MysteryGenerationState) -> MysteryGenerationState:
    """Generate characters for the mystery game."""
    llm = get_llm()

    system_prompt = """You are an expert mystery writer creating characters for a murder mystery party game.
Generate diverse, interesting characters with distinct personalities, backgrounds, and secrets.
Each character should have a plausible connection to the mystery."""

    user_prompt = f"""Create {state['num_players']} LIVING player characters for a mystery party game with the following parameters:
- Theme: {state['theme']}
- Difficulty: {state['difficulty']}
{f"- Special requests: {state['special_requests']}" if state.get('special_requests') else ""}

IMPORTANT: These are the PLAYABLE characters who will investigate the murder. They are all ALIVE at the start of the game.
The victim will be a separate NPC (non-player character) defined later in the plot.

For each LIVING character, provide:
- name: Full name
- role: Their occupation or role
- background: Brief background story (2-3 sentences)
- personality: Key personality traits
- secret: A hidden secret they're keeping
- motive: A potential motive for murder (at least one character should be the future culprit)
- relationship_to_victim: How they know the victim (will be defined in the plot)

Return the response as a JSON array of character objects."""

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
    except Exception as e:
        print(f"Error parsing characters: {e}")
        print(f"Response content: {response.content[:500]}")  # Print first 500 chars for debugging
        state["characters"] = []

    return state
