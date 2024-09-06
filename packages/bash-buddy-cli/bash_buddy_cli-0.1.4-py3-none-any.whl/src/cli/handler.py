from .commands import handle_question, handle_api_key

def handle_arguments(args):
    """
    Handles the parsed arguments and calls the appropriate command handler for question and API key.

    Args:
        args (argparse.Namespace): Parsed arguments.
    """
    if args.question:
        handle_question(args.question)
    if args.api_key:
        handle_api_key(args.api_key)
    if not args.question and not args.api_key:
        print("No valid command provided.")
