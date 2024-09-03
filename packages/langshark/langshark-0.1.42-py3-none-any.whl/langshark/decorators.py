from functools import wraps
from .client import get_global_client

def observe(**langfuse_kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            global_client = get_global_client()
            callback_handler = global_client.callback_handler

            # Use the Langfuse CallbackHandler directly
            with callback_handler.as_span(**langfuse_kwargs):
                try:
                    # Execute the function
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    # The error will be automatically captured by the span
                    raise

        return wrapper
    return decorator