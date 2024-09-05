import argparse

def create_parser():
    """
    Creates and returns the argument parser for the CLI.

    Returns:
        argparse.ArgumentParser: Configured argument parser.
    """
    parser = argparse.ArgumentParser(description="A cli tool to give you a helpful question asnwering buddy in the terminal.")

    # Add question argument to the parser
    parser.add_argument(
        'question',
        type=str,
        nargs='?',
        help='Question to process'
    )

    
    parser.add_argument(
        '--api_key',
        type=str,
        required=False,
        help='Add API key for ChatGPT integration'
    )

    return parser
