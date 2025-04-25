import os
from dotenv import load_dotenv
load_dotenv()
import logfire
from tasks.agents_test.search_agent_test import run_search_task

# Initialize logfire (will use LOGFIRE_TOKEN from .env)
logfire.configure()

if __name__ == "__main__":
    logfire.info("Starting test run from main.py")
    run_search_task()