"""Plot generation node."""

import json
from langchain_core.messages import SystemMessage, HumanMessage
from src.models.state import MysteryGenerationState
from src.models.schema import Plot
from src.graph.nodes.utils import get_llm


def generate_plot_node(state: MysteryGenerationState) -> MysteryGenerationState:
    """Generate the main plot and storyline."""
    llm = get_llm()

    characters_summary = "\n".join([
        f"- {char.name} ({char.role}): {char.background}"
        for char in state.get("characters", [])
    ])

    system_prompt = """You are an expert mystery writer creating compelling murder mystery plots.
Create a coherent, engaging plot that ties all characters together with a satisfying resolution."""

    user_prompt = f"""Create a murder mystery plot for a party game with these parameters:
- Theme: {state['theme']}
- Difficulty: {state['difficulty']}

Living player characters (all playable suspects/investigators):
{characters_summary}

Provide a JSON object with these exact fields:
- setting: STRING - Detailed setting description combining time, place, and atmosphere (2-3 sentences)
- victim: STRING - Name of the victim (must be an NPC, NOT one of the player characters listed above. Create a new character name for the victim)
- crime: STRING - Description of the crime
- culprit: STRING - Name of the culprit (MUST be one of the player characters listed above)
- murder_method: STRING - How the crime was committed
- timeline: ARRAY of STRINGS - 5-8 key events in chronological order (the murder should occur BEFORE the game starts)
- resolution: STRING - How the mystery can be solved

IMPORTANT:
1. Return ONLY a valid JSON object. The 'setting' field must be a single string, not an object.
2. The VICTIM must be an NPC (not a player character).
3. The CULPRIT must be one of the player characters listed above.
4. The victim is already DEAD when the game starts. The timeline should show the murder happened before gameplay begins."""

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
    except Exception as e:
        print(f"Error parsing plot: {e}")
        print(f"Response content: {response.content[:500]}")  # Print first 500 chars for debugging
        state["plot"] = None

    return state
