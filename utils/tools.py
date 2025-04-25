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
            model=f"openai/{model}",  # Add provider prefix as per documentation
            temperature=0.7,
            api_key=api_key
        )
        return llm

    elif provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Missing GEMINI_API_KEY in environment variables.")
        
        # Get model name from environment variable or default to "gemini-1.5-pro"
        model_name = os.getenv("GEMINI_LLM", "gemini-1.5-pro")
        print('found gemini', model_name)
        # For direct Gemini API access, use the "gemini/" prefix
        # Do not use "vertex_ai/" as that requires Google Cloud credentials
        if not model_name.startswith("gemini/"):
            model_string = f"gemini/{model_name}"
        else:
            model_string = model_name
        
        print(f"Using model: {model_string}")
        
        # Create CrewAI LLM instance
        llm = LLM(
            model=model_string,
            temperature=0.7,
            api_key=api_key
        )
        
        return llm

    elif provider == "claude":
        # Future Claude integration placeholder
        raise NotImplementedError("Claude provider is not yet implemented.")

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
