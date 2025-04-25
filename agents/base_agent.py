# agents/base_agent.py
from utils.tools import get_llm_client
from dotenv import load_dotenv
import os
from typing import List, Optional
from crewai import Agent, LLM
from .llm_config import LLMConfig

load_dotenv()

class BaseAgent:
    """Base class for all agents in the system, providing common properties and methods."""
    def __init__(self, role: str, goal: str, backstory: str, tools: Optional[List] = None, allow_delegation: bool = False):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools or []
        self.allow_delegation = allow_delegation
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
        print(f"Using model: {model_string}")
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
        Handles both direct Gemini models and CrewAI LLM instances.
        """
        if not self.llm_client:
            raise ValueError(f"LLM client not initialized. Check if {self.llm_provider.upper()}_API_KEY is set.")
            
        # Handle different LLM client types
        try:
            # Check if this is a CrewAI LLM instance with call method
            if hasattr(self.llm_client, 'call') and callable(getattr(self.llm_client, 'call')):
                print('calling Crew ai call')
                # CrewAI LLM uses call() method with a messages parameter
                messages = [{"role": "user", "content": prompt}]
                response = self.llm_client.call(messages=messages)
                return response
            
            # Google's GenerativeModel
            elif hasattr(self.llm_client, 'generate_content') and callable(getattr(self.llm_client, 'generate_content')):
                response = self.llm_client.generate_content(prompt)
                return response.text
            
            # OpenAI and other chat-based APIs
            elif hasattr(self.llm_client, 'chat'):
                response = self.llm_client.chat([{"role": "user", "content": prompt}])
                return response['choices'][0]['message']['content']
            
            # If none of the above patterns match, raise an error
            else:
                raise ValueError(f"Unsupported LLM client type: {type(self.llm_client).__name__}. Available methods: {dir(self.llm_client)}")
                
        except Exception as e:
            raise ValueError(f"Error communicating with LLM: {str(e)}")
