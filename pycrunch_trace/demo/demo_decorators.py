import logging
import functools
from pycrunch_trace.client.api import trace

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='pycrunch-trace | %(asctime)s | %(levelname)-8s | %(message)s'
)

def dummy_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("--- Entering Dummy Decorator ---")
        result = func(*args, **kwargs)
        print("--- Exiting Dummy Decorator ---")
        return result
    return wrapper

@trace
@dummy_decorator
def tracked_function_outer():
    """
    When @trace is OUTSIDE (above), it records:
    1. The entry into tracked_function_outer
    2. The execution of the dummy_decorator wrapper
    3. The execution of the original function body
    """
    print("Executing tracked_function_outer body")

@dummy_decorator
@trace
def tracked_function_inner():
    """
    When @trace is INSIDE (below), it records ONLY:
    1. The execution of the original function body
    (The dummy_decorator is NOT tracked because it wraps the tracked function)
    """
    print("Executing tracked_function_inner body")

if __name__ == "__main__":
    print("\n>>> Scenario 1: @trace is outermost")
    tracked_function_outer()
    
    print("\n>>> Scenario 2: @trace is innermost")
    tracked_function_inner()
