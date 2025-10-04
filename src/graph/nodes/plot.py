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

Characters involved:
{characters_summary}

Provide:
- setting: Detailed setting (time and place)
- victim: Name of the victim (should be one of the characters)
- crime: Description of the crime
- culprit: Who committed the crime (should be one of the characters)
- murder_method: How the crime was committed
- timeline: Array of key events (5-8 events)
- resolution: How the mystery can be solved

Return the response as a JSON object."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    response = llm.invoke(messages)

    try:
        plot_data = json.loads(response.content)
        plot = Plot(**plot_data)
        state["plot"] = plot
    except Exception as e:
        print(f"Error parsing plot: {e}")
        state["plot"] = None

    return state
