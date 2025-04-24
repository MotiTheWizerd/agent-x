# Agent-X

A modular team of autonomous agents using CrewAI, Pydantic, and PydanticAI, designed to collaborate on structured tasks.

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the package in development mode:

```bash
pip install -e .
```

3. Set up environment variables in `.env`:

```
BRAVE_API_KEY=your_brave_api_key
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
DEFAULT_LLM_PROVIDER=openai  # or gemini
```

## Running Tests

To test the search agent:

```bash
python tasks/agents_test/search_agent_test.py
```

## Project Structure

- `agents/`: Contains all agent implementations
- `utils/`: Utility functions and tools
- `tasks/`: Task definitions and agent workflows
- `prompts/`: Prompt templates for agents
- `config/`: Configuration settings

## License

MIT
