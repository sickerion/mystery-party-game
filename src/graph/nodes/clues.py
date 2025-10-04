"""Clues generation node."""

import json
from langchain_core.messages import SystemMessage, HumanMessage
from src.models.state import MysteryGenerationState
from src.models.schema import Clue
from src.graph.nodes.utils import get_llm


def generate_clues_node(state: MysteryGenerationState) -> MysteryGenerationState:
    """Generate clues for the mystery."""
    llm = get_llm()

    plot_summary = ""
    if state.get("plot"):
        plot = state["plot"]
        plot_summary = f"""
Victim: {plot.victim}
Culprit: {plot.culprit}
Method: {plot.murder_method}
Setting: {plot.setting}
"""

    characters_list = ", ".join([char.name for char in state.get("characters", [])])

    system_prompt = """You are an expert mystery writer creating clues for a murder mystery game.
Create a mix of helpful clues and red herrings that make the mystery challenging but solvable."""

    user_prompt = f"""Create clues for a murder mystery game with these parameters:
- Theme: {state['theme']}
- Difficulty: {state['difficulty']}
- Number of clues: {state['num_players'] + 3}

Plot details:
{plot_summary}

Characters: {characters_list}

For each clue provide:
- clue_id: Unique identifier (e.g., "clue_001")
- description: What the clue is
- location: Where it's found
- revealed_by: Which character has or reveals this clue
- significance: Why it's important
- misleading: Boolean - is this a red herring?

Return the response as a JSON array of clue objects."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    response = llm.invoke(messages)

    try:
        clues_data = json.loads(response.content)
        clues = [Clue(**clue) for clue in clues_data]
        state["clues"] = clues
    except Exception as e:
        print(f"Error parsing clues: {e}")
        state["clues"] = []

    return state
