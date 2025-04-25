# agents/search_agent.py
import os
import logfire  # Add logfire import
from typing import Dict, List, Any
from agents.base_agent import BaseAgent
from utils.brave_search_tool import BraveSearchTool

class SearchAgent(BaseAgent):
    """
    SearchAgent is responsible for performing internet searches and retrieving relevant information.
    It uses the Brave Search API for web searches.
    """
    def __init__(self, name: str = "Search Specialist", verbose: bool = True):
        # Define required properties for BaseAgent
        role = "Web search Specialist"
        goal = "Find accurate and relevant information from the web based on queries"
        backstory = "As a search specialist, I have been trained to efficiently find information on the internet, analyzing search results to provide the most relevant data. I specialize in contextual understanding of search queries and retrieving high-quality information."
        super().__init__(name=name, role=role, goal=goal, backstory=backstory)
        
        # Validate API key
        if not os.getenv("BRAVE_API_KEY"):
            raise ValueError("BRAVE_API_KEY environment variable is required for SearchAgent")
        
        # Initialize search tool
        self.search_tool = BraveSearchTool()
        
        self.verbose = verbose

    def perform_task(self, query: str) -> List[Dict[str, str]]:
        """
        Performs a search using the provided query and returns the results.
        
        Args:
            query: The search query string
            
        Returns:
            A list of search results, each containing title, url, and description
        """
        logfire.info("Search started", agent=self.name, query=query)
        if self.verbose:
            print("\n" + "="*50)
            print(f"🔍 Agent: {self.name} ({self.role})")
            print(f"🎯 Goal: {self.goal}")
            print(f"🤔 Thinking: I'll search for information about: '{query}'")
            print(f"🛠️ Using tool: brave_search")
            print("="*50 + "\n")
        
        try:
            # Execute the search
            if self.verbose:
                print(f"🔎 Executing search query: '{query}'")
                
            search_results = self.search_tool.search(query)
            logfire.info("Search completed", agent=self.name, query=query, result_count=len(search_results))
            
            if self.verbose:
                print(f"✅ Found {len(search_results)} results")
                if len(search_results) > 0 and "error" in search_results[0]:
                    print(f"❌ Error: {search_results[0]['error']}")
            
            # LLM analysis enabled to enhance search results with summary
            try:
                prompt = f"""
                Analyze the following search results for the query: '{query}'
                
                {search_results[:3]}
                
                Provide a brief summary of the key information found:
                """
                analysis = self.interact_with_llm(prompt)
                if self.verbose:
                    print(f"\n📊 Analysis: {analysis}\n")
            except Exception as e:
                logfire.error("LLM analysis failed", agent=self.name, query=query, error=str(e))
                if self.verbose:
                    print(f"⚠️ LLM analysis skipped: {str(e)}")
            
            return search_results
        except Exception as e:
            error_msg = f"Search failed: {str(e)}"
            logfire.error("Search failed", agent=self.name, query=query, error=str(e))
            if self.verbose:
                print(f"❌ {error_msg}")
            return [{"error": error_msg}]
    
    def get_agent_info(self) -> Dict[str, Any]:
        """
        Returns information about this agent for use in CrewAI or other frameworks.
        
        Returns:
            Dictionary containing agent information
        """
        return {
            "name": self.name,
            "role": self.role,
            "goal": self.goal,
            "backstory": self.backstory,
            "verbose": self.verbose
        }
