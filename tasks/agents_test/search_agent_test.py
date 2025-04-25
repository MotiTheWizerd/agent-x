# tasks/agents_test/search_agent_test.py
import os
import sys
import json
from dotenv import load_dotenv
from agents.search_agent import SearchAgent

print("Script started...")

def run_search_task(query=None, verbose=True):
    """
    Run a test of the SearchAgent with the specified query.
    
    Args:
        query: Optional search query (defaults to test query if None)
        verbose: Whether to enable verbose mode in the agent
    """
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    # Check if BRAVE_API_KEY is set
    brave_api_key = os.getenv("BRAVE_API_KEY")
    if not brave_api_key:
        print("Error: BRAVE_API_KEY environment variable is not set.")
        print("Please set it before running this test.")
        sys.exit(1)
    
    # Initialize the SearchAgent
    try:
        print("\n🔍 Initializing SearchAgent...")
        agent = SearchAgent(verbose=verbose)
        
        # Only print agent info if not in verbose mode (otherwise would be redundant)
        if not verbose:
            agent_info = agent.get_agent_info()
            print("\nAgent Information:")
            print(f"Role: {agent_info['role']}")
            print(f"Goal: {agent_info['goal']}")
            print(f"Tools: {', '.join(agent_info['tools'])}")
            print(f"Tags: {', '.join(agent_info['tags'])}")

        # Use provided query or default test query
        search_query = query or "can you please find me some good and cheap places to buy food for home (not restaurant) in israel, i live Ha Shive street in tel aviv?"
        
        if not verbose:
            print(f"\nPerforming search for: '{search_query}'")
            
        # Perform the search
        search_results = agent.perform_task(search_query)
        
        # Display the search results
        if not search_results:
            print("❌ No search results returned.")
            sys.exit(1)
            
        if isinstance(search_results, list) and len(search_results) > 0 and "error" in search_results[0]:
            print(f"❌ Search error: {search_results[0]['error']}")
            sys.exit(1)
        
        # Display results in a nicely formatted way
        print("\n" + "="*70)
        print(f"🔎 SEARCH RESULTS: '{search_query}'")
        print(f"📊 Found {len(search_results)} results")
        print("="*70)
        
        for idx, result in enumerate(search_results, 1):
            print(f"\n{idx}. {result.get('title', 'No title')}")
            print(f"   🔗 {result.get('url', 'No URL')}")
            print(f"   📝 {result.get('description', 'No description')}")
            
        print("\n" + "="*70)
        print("✅ Test completed successfully!")
        print("="*70)
        
        # Return the results for further processing if needed
        return search_results
        
    except Exception as e:
        print(f"❌ Error running search test: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check if a custom query was provided as a command-line argument
    custom_query = None
    verbose_flag = True
    
    # Parse command line arguments
    for arg in sys.argv[1:]:
        if arg.startswith("--query="):
            custom_query = arg.split("=", 1)[1]
        elif arg == "--no-verbose":
            verbose_flag = False
    
    # Run the search with the provided query or default
    run_search_task(query=custom_query, verbose=verbose_flag)
