from config.config import add_api_key_to_env
from llm_integration.openai_integration import chat_with_openai

def handle_question(question):
    """
    Handles the input question command by sending it to OpenAI's GPT-4 model and printing the response.
    
    Args:
        question (str): The question to process.
    """
    try:
        response = chat_with_openai(question)
        print(f"Response from OpenAI: {response}")
    except Exception as e:
        print(f"Error: {e}")

def handle_api_key(api_key):
    """
    Handles the API key argument by adding it to the environment variables.

    Args:
        api_key (str): The API key for ChatGPT integration.
    """
    try:
        add_api_key_to_env(api_key)
        print(f"API key added to environment: {api_key}")
    except ValueError as e:
        print(f"Error: {e}")