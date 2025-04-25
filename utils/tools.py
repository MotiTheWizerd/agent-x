import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

def get_llm_client(provider: str = "gemini"):
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_LLM", "gpt-4")
        if not api_key:
            raise ValueError("Missing OPENAI_API_KEY in environment variables.")
        # Use CrewAI's LLM for OpenAI
        llm = LLM(
            model=model,
            temperature=0.7,
            api_key=api_key
        )
        return llm

    elif provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Missing GEMINI_API_KEY in environment variables.")
        
        # Get model string from environment variable or default to "gemini/gemini-1.5-pro"
        model_string = os.getenv("GEMINI_LLM", "gemini/gemini-1.5-pro")
        
        # Create CrewAI LLM instance
        llm = LLM(
            model=model_string,
            temperature=0.7,
        )
        
        return llm

    elif provider == "claude":
        # Future Claude integration placeholder
        raise NotImplementedError("Claude provider is not yet implemented.")

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
