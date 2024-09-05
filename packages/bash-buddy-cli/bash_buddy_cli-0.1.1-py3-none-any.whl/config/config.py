from dotenv import load_dotenv
import os

def load_env_variables():
    """
    Load environment variables from a .env file.
    """
    load_dotenv()

def get_api_key():
    """
    Retrieve the API key from the environment variables.
    
    Returns:
        str: The API key.
    
    Raises:
        ValueError: If the API key is not found in the environment variables.
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("API_KEY not found. Please run -h & add it")
    return api_key

def ensure_env_file_exists():
    """
    Ensure that the .env file exists in the project root directory. If it does not exist, create an empty one.
    """
    env_path = os.path.join(os.path.dirname(__file__), '../../.env')
    if not os.path.exists(env_path):
        with open(env_path, 'w') as env_file:
            env_file.write('')  # Create an empty .env file

def read_env_file(env_path):
    """
    Read the contents of the .env file.
    
    Args:
        env_path (str): The path to the .env file.
    
    Returns:
        list: The lines of the .env file.
    """
    with open(env_path, 'r') as env_file:
        return env_file.readlines()

def write_env_file(env_path, lines):
    """
    Write the given lines to the .env file.
    
    Args:
        env_path (str): The path to the .env file.
        lines (list): The lines to write to the .env file.
    """
    with open(env_path, 'w') as env_file:
        env_file.writelines(lines)

def add_api_key_to_env(api_key):
    """
    Add the API key to the .env file, replacing any existing key.
    
    Args:
        api_key (str): The API key to be added.
    
    Raises:
        ValueError: If the API key is empty or None.
    """
    if not api_key:
        raise ValueError("API key cannot be empty or None.")
    
    ensure_env_file_exists()  # Ensure .env file exists before writing to it

    env_path = os.path.join(os.path.dirname(__file__), '../../.env')
    
    # Read the current contents of the .env file
    lines = read_env_file(env_path)
    
    # Write back to the .env file, replacing the API key if it exists
    key_written = False
    new_lines = []
    for line in lines:
        if line.startswith('OPENAI_API_KEY='):
            new_lines.append(f'OPENAI_API_KEY={api_key}\n')
            key_written = True
        else:
            new_lines.append(line)
    
    # If the key was not found, append it to the file
    if not key_written:
        new_lines.append(f'\nOPENAI_API_KEY={api_key}\n')
    
    write_env_file(env_path, new_lines)
    
    load_env_variables()  # Reload the environment variables to include the new API key