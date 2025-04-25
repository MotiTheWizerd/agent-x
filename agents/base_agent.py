# agents/base_agent.py
from utils.tools import get_llm_client
from dotenv import load_dotenv
import os

load_dotenv()

class BaseAgent:
    def __init__(self, name: str, llm_provider: str = None):
        self.name = name
        self.llm_provider = llm_provider or os.getenv("DEFAULT_LLM_PROVIDER", "gemini")
        try:
            self.llm_client = get_llm_client(self.llm_provider)
        except ValueError as e:
            # Log the error but don't fail initialization if the agent doesn't need LLM
            print(f"Warning: LLM client initialization failed: {str(e)}")
            print(f"The agent will initialize, but LLM-dependent features won't work.")
            self.llm_client = None
        except Exception as e:
            # Catch other exceptions for better error reporting
            print(f"Warning: LLM client initialization error: {str(e)}")
            print(f"The agent will initialize, but LLM-dependent features won't work.")
            self.llm_client = None

    def perform_task(self, task_input: str):
        # Example: You can implement this in subclasses of BaseAgent
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
