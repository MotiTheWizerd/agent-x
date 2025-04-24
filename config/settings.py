import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LLM Provider Settings
DEFAULT_LLM_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "gemini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")

# Brave Search Settings
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
BRAVE_SEARCH_COUNT = int(os.getenv("BRAVE_SEARCH_COUNT", "10"))

# Logging Settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
