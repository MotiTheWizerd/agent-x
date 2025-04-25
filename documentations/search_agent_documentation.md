# SearchAgent Documentation

## Overview

`SearchAgent` is a specialized agent in the Agent-X framework designed to perform internet searches and retrieve relevant information using the Brave Search API. It extends `BaseAgent` and adds search-specific logic and tools, making it ideal for tasks that require up-to-date web data.

---

## Class: `SearchAgent`

**Location:** `agents/search_agent.py`

### Purpose

- Performs web searches using the Brave Search API.
- Analyzes and summarizes search results using an LLM.
- Provides a reusable, extensible agent for information retrieval tasks.

---

## Attributes

- `name` (str): Human-readable name for the agent (default: "Search Specialist").
- `role` (str): The agent's role (default: "Web search Specialist").
- `goal` (str): The agent's main objective (default: "Find accurate and relevant information from the web based on queries").
- `backstory` (str): Narrative context for the agent's behavior.
- `search_tool` (`BraveSearchTool`): Tool instance for performing Brave web searches.
- `verbose` (bool): If True, prints detailed logs during operation.

---

## Key Methods

### `__init__(...)`

Initializes the agent with a name, sets up the Brave Search tool, and validates the required API key.

### `perform_task(query: str) -> List[Dict[str, str]]`

Executes a web search for the given query, prints/logs the process if verbose, and returns a list of search results. Also attempts to summarize results using the LLM.

### `get_agent_info() -> Dict[str, Any>`

Returns a dictionary with the agent's configuration and metadata (name, role, goal, backstory, verbose).

---

## Usage Example

```python
from agents.search_agent import SearchAgent

# Instantiate the agent
agent = SearchAgent(verbose=True)

# Perform a search
results = agent.perform_task("latest AI research trends")

# Print results
for result in results:
    print(result)
```

---

## Extension & Customization

- **Subclassing:** Inherit from `SearchAgent` to add custom search logic or integrate additional tools.
- **API Key:** Ensure `BRAVE_API_KEY` is set in your `.env` file for the Brave Search API.
- **Verbose Mode:** Use the `verbose` flag for detailed logs during development or debugging.

---

## Notes

- `SearchAgent` depends on `BraveSearchTool` (see `utils/brave_search_tool.py`).
- LLM-based analysis is optional and will be skipped if the LLM is not available or fails.
- For more details, see the source code in `agents/search_agent.py`.
