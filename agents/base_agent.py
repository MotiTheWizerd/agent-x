# agents/base_agent.py
from dotenv import load_dotenv
import os
from typing import List, Optional
from crewai import Agent, LLM
from .llm_config import LLMConfig

load_dotenv()

class BaseAgent:
    """Base class for all agents in the system, providing common properties and methods."""
    def __init__(self, role: str, goal: str, backstory: str, tools: Optional[List] = None, allow_delegation: bool = False, name: str = 'Base Agent'):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools or []
        self.allow_delegation = allow_delegation
        self.name = name
        # Grouped LLM configuration as a single field with default values
        self.llm_config = LLMConfig()

    def get_llm(self) -> LLM:
        """Create and return a configured CrewAI LLM instance based on the agent's config."""
        config_dict = self.llm_config.to_dict()
        # Ensure API key is set based on provider in model string
        model_string = config_dict.get('model', os.getenv("LLM_PROVIDER_MODEL", "gemini/gemini-1.5-pro"))
        provider = model_string.split('/')[0]
        api_key_map = {
            "openai": "OPENAI_API_KEY",
            "gemini": "GEMINI_API_KEY"
            # Add more providers here as needed
        }
        if provider not in api_key_map:
            raise ValueError(f"Unsupported LLM provider in model string: {provider}")
        api_key_name = api_key_map[provider]
        api_key = os.getenv(api_key_name)
        if not api_key:
            raise ValueError(f"Missing {api_key_name} in environment variables.")
        config_dict.setdefault('api_key', api_key)
        # Commented out to reduce console clutter
        # print(f"Using model: {model_string}")
        return LLM(**config_dict)

    def get_agent(self) -> Agent:
        """Create and return a CrewAI Agent instance with the configured settings."""
        return Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            tools=self.tools,
            allow_delegation=self.allow_delegation,
            llm=self.get_llm(),
        )

    def customize_llm(self, **kwargs):
        """Customize LLM parameters by updating the config object."""
        for key, value in kwargs.items():
            if hasattr(self.llm_config, key):
                setattr(self.llm_config, key, value)
            else:
                raise ValueError(f"Invalid LLM parameter: {key}")

    def perform_task(self, task_input: str):
        """Example method to be implemented in subclasses."""
        raise NotImplementedError("Each agent must implement the `perform_task` method.")

    def interact_with_llm(self, prompt: str):
        """
        Send prompt to the LLM and get the response.
        Uses the configured CrewAI LLM instance from get_llm().
        """
        # Use the LLM instance from get_llm() for interaction
        llm_instance = self.get_llm()
        
        # Handle interaction with the CrewAI LLM instance
        try:
            print('Calling CrewAI LLM')
            messages = [{"role": "user", "content": prompt}]
            response = llm_instance.call(messages=messages)
            return response
        except Exception as e:
            raise ValueError(f"Error communicating with LLM: {str(e)}")
