import traceback
import datetime

def handle_error(function_name, error):
    """
    Handles errors and prints a formatted message with more clarity.

    :param function_name: The name of the function where the error occurred.
    :param error: The exception object.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp
    error_type = type(error).__name__  # Get error type (e.g., KeyError, ValueError)

    print("\n" + "="*60)
    print(f"ERROR OCCURRED")
    print("="*60)
    print(f"Function: {function_name}")
    print(f"⚠️  Error Type: {error_type}")
    print(f"💡 Message: {str(error)}")
    print("\n🔍 Full Traceback:")
    print(traceback.format_exc())  # Prints detailed error traceback
    print("="*60 + "\n")
