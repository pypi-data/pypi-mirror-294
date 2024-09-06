import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cli.parser import create_parser
from cli.handler import handle_arguments
from config.config import load_env_variables



def main():
    """
    Main function to load environment variables, parse arguments, and execute the appropriate actions.
    """
    
    # Load environment variables
    load_env_variables()
    
    # Create the argument parser
    parser = create_parser()
    
    # Parse the command line arguments
    args = parser.parse_args()
    
    # Handle the parsed arguments
    handle_arguments(args)

if __name__ == "__main__":
    main()
