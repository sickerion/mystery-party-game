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

    user_prompt = f"""Create {state['num_players']} characters for a mystery party game with the following parameters:
- Theme: {state['theme']}
- Difficulty: {state['difficulty']}
{f"- Special requests: {state['special_requests']}" if state.get('special_requests') else ""}

For each character, provide:
- name: Full name
- role: Their occupation or role
- background: Brief background story (2-3 sentences)
- personality: Key personality traits
- secret: A hidden secret they're keeping
- motive: A potential motive (for some characters)
- relationship_to_victim: How they know the victim (if applicable)

Return the response as a JSON array of character objects."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    response = llm.invoke(messages)

    # Parse the response and create Character objects
    try:
        characters_data = json.loads(response.content)
        characters = [Character(**char) for char in characters_data]
        state["characters"] = characters
    except Exception as e:
        print(f"Error parsing characters: {e}")
        state["characters"] = []

    return state
