# BaseAgent Documentation

## Overview

`BaseAgent` is the foundational class for all agents in the Agent-X framework. It provides common properties, LLM configuration, and utility methods that specialized agents inherit and extend. This ensures consistency, modularity, and ease of maintenance across all agent types.

---

## Class: `BaseAgent`

**Location:** `agents/base_agent.py`

### Purpose

- Encapsulates shared logic for agent configuration, LLM setup, and agent instantiation.
- Serves as the superclass for all custom agents in the system.

---

## Attributes

- `role` (str): The agent's role or function (e.g., "IDE Assistant").
- `goal` (str): The primary objective or mission of the agent.
- `backstory` (str): Context or narrative for the agent's behavior.
- `tools` (List, optional): List of tools or capabilities the agent can use.
- `allow_delegation` (bool): Whether the agent can delegate tasks to others.
- `name` (str): Human-readable name for the agent.
- `llm_config` (`LLMConfig`): Configuration object for the agent's LLM (model, provider, etc.).

---

## Key Methods

### `__init__(...)`

Initializes the agent with its role, goal, backstory, tools, delegation flag, and name. Sets up a default LLM configuration.

### `get_llm()`

Returns a configured CrewAI LLM instance based on the agent's LLM config and environment variables. Handles provider selection and API key management.

### `get_agent()`

Creates and returns a CrewAI `Agent` instance with the agent's settings and LLM.

### `customize_llm(**kwargs)`

Allows dynamic updates to the LLM configuration (e.g., model, temperature) by passing keyword arguments.

### `perform_task(task_input: str)`

Abstract method to be implemented by subclasses. Defines the agent's main task logic.

### `interact_with_llm(prompt: str)`

Sends a prompt to the configured LLM and returns the response. Handles errors gracefully.

---

## Usage Example

```python
from agents.base_agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Example Agent",
            goal="Demonstrate base agent usage",
            backstory="A test agent for documentation purposes."
        )

    def perform_task(self, task_input: str):
        return self.interact_with_llm(f"Task: {task_input}")

# Instantiate and use the agent
agent = MyAgent()
result = agent.perform_task("Summarize this text.")
print(result)
```

---

## Extension & Customization

- **Subclassing:** Inherit from `BaseAgent` to create specialized agents. Implement the `perform_task` method for custom logic.
- **LLM Customization:** Use `customize_llm()` to adjust model parameters at runtime.
- **Tools:** Pass a list of tools to the constructor to extend agent capabilities.

---

## Notes

- Ensure required API keys are set in your `.env` file for the chosen LLM provider.
- All agents should inherit from `BaseAgent` for consistency and maintainability.
- For more details, see the source code in `agents/base_agent.py`.
