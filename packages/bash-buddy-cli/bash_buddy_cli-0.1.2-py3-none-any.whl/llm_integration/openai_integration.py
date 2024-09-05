from openai import OpenAI
from config.config import get_api_key

def chat_with_openai(question):
    """
    Function to chat with OpenAI's GPT-4 model and get a response to a question about bash.
    
    Parameters:
    question (str): The question to ask the OpenAI model.
    
    Returns:
    str: The response from the OpenAI model.
    """
    # Retrieve the API key from environment variables
    api_key = get_api_key()
    
    # Initialize the OpenAI client with the API key
    client = OpenAI(api_key=api_key)

    # Define the messages to be sent to the model
    messages = [
        {"role": "system", "content": "You are a helpful assistant knowledgeable about bash scripting. Your purpose is to help the user in their linux terminal & answer their questions relating to bash commands & the terminal. You are to be as concise as possible, delivering only the necessary information. Always include examples or the direct commands the user needs to accomplish their goal."},
        {"role": "user", "content": question}
    ]

    # Make the API call to OpenAI's chat completions endpoint
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    # Extract and return the assistant's response
    return response.choices[0].message.content
