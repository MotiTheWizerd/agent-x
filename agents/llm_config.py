from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
import os

class LLMConfig(BaseModel):
    """Configuration class for LLM parameters with default values for CrewAI agents."""
    model: str = Field(default=os.getenv('DEFAULT_LLM', 'gemini/gemini-2.0-flash-exp'))
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(default=4000, ge=1)
    top_p: float = 0.9
    frequency_penalty: float = 0.1
    presence_penalty: float = 0.1
    timeout: int = Field(default=120, ge=1)
    response_format: Optional[Dict[str, Any]] = None  # e.g., {"type": "json"}
    # Commented out parameters below may not be universally supported across all LLM providers in CrewAI
    # seed: Optional[int] = None  # For reproducible results, may not work with all providers
    # stop: Optional[List[str]] = None  # Sequences to stop generation, support varies by provider
    # base_url: Optional[str] = None  # Custom API endpoint if needed, for specific setups

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary for easy passing to LLM initialization.
        Excludes None values to avoid passing unset parameters."""
        return self.model_dump(exclude_none=True) 