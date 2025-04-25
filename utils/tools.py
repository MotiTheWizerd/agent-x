import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

# Commented out functions below are unused in the current implementation
# They replicate logic handled by BaseAgent.get_llm() and LLMConfig
# Keep for potential future use or alternative LLM client creation
# def create_llm_client(provider: str = "gemini", temperature: float = 0.7):
#     """
#     Create a basic LLM client using CrewAI's LLM abstraction for non-agent use cases.
#     The model string is read from environment variables or defaults to a provider-specific model.
#     
#     Args:
#         provider (str): The provider to use, defaults to 'gemini'. Used as fallback if model string is not set.
#         temperature (float, optional): The temperature setting for the LLM. Defaults to 0.7.
#     Returns:
#         LLM: A configured CrewAI LLM instance.
#     """
#     # Read the full model string from environment or set default based on provider
#     model_string = os.getenv("LLM_PROVIDER_MODEL", f"{provider}/{provider}-1.5-pro" if provider == "gemini" else f"{provider}/gpt-4o-mini")
#     
#     # Extract provider from the model string
#     provider = model_string.split('/')[0]
#     
#     # Map provider to the appropriate API key environment variable
#     api_key_map = {
#         "openai": "OPENAI_API_KEY",
#         "gemini": "GEMINI_API_KEY"
#         # Add more providers here as needed
#     }
#     
#     if provider not in api_key_map:
#         raise ValueError(f"Unsupported LLM provider in model string: {provider}")
#     
#     api_key_name = api_key_map[provider]
#     api_key = os.getenv(api_key_name)
#     if not api_key:
#         raise ValueError(f"Missing {api_key_name} in environment variables.")
#     
#     # Commented out to reduce console clutter
#     # print(f"Using model: {model_string}")
#     
#     # Create CrewAI LLM instance with minimal configuration
#     llm = LLM(
#         model=model_string,
#         temperature=temperature,
#         api_key=api_key
#     )
#     
#     return llm

# def get_llm_client(provider: str = "gemini", temperature: float = None):
#     """
#     Get an LLM client using CrewAI's LLM abstraction. The model string is read directly
#     from environment variables with provider prefix (e.g., 'openai/gpt-4' or 'gemini/gemini-1.5-pro').
#     
#     Args:
#         provider (str): The provider to use, defaults to 'gemini'. This is used as a fallback if the model string is not set.
#         temperature (float, optional): The temperature setting for the LLM to control randomness/creativity.
#             If provided, it is used as specified (typically from agent configuration or override). Defaults to None,
#             which will use CrewAI's default temperature if not set by the caller.
#     Returns:
#         LLM: A configured CrewAI LLM instance.
#     """
#     # Read the full model string (with provider prefix) from environment
#     model_string = os.getenv("LLM_PROVIDER_MODEL", "gemini/gemini-1.5-pro")
#     
#     # Extract provider from the model string (e.g., 'openai' from 'openai/gpt-4')
#     provider = model_string.split('/')[0]
#     
#     # Map provider to the appropriate API key environment variable
#     api_key_map = {
#         "openai": "OPENAI_API_KEY",
#         "gemini": "GEMINI_API_KEY"
#         # Add more providers here as needed
#     }
#     
#     if provider not in api_key_map:
#         raise ValueError(f"Unsupported LLM provider in model string: {provider}")
#     
#     api_key_name = api_key_map[provider]
#     api_key = os.getenv(api_key_name)
#     if not api_key:
#         raise ValueError(f"Missing {api_key_name} in environment variables.")
#     
#     # Commented out to reduce console clutter
#     # print(f"Using model: {model_string}")
#     
#     # Create CrewAI LLM instance with the model string, API key, and provided temperature
#     # Temperature is passed as-is; defaults or agent-specific values are handled by the caller
#     llm = LLM(
#         model=model_string,
#         temperature=temperature,
#         api_key=api_key
#     )
#     
#     return llm

# Removed stray variable references that were causing NameError 