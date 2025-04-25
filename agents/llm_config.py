from dataclasses import dataclass
from typing import Dict, Any, Optional, List

@dataclass
class LLMConfig:
    """Configuration class for LLM parameters with default values for CrewAI agents."""
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 4000
    top_p: float = 0.9
    frequency_penalty: float = 0.1
    presence_penalty: float = 0.1
    timeout: int = 120
    response_format: Optional[Dict[str, Any]] = None  # e.g., {"type": "json"}
    seed: Optional[int] = None  # For reproducible results
    stop: Optional[List[str]] = None  # Sequences to stop generation
    base_url: Optional[str] = None  # Custom API endpoint if needed

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary for easy passing to LLM initialization.
        Excludes None values to avoid passing unset parameters."""
        return {k: v for k, v in vars(self).items() if not k.startswith('_') and v is not None} 