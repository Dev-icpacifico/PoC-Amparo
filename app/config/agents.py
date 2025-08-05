from typing import Literal

# Define available LLM types
LLMType = Literal["basic", "reasoning"]

# Define agent-LLM mapping
AGENT_LLM_MAP: dict[str, LLMType] = {
    "amparo": "basic",
    "supervisor": "basic",
    "consultas": "reasoning",
}