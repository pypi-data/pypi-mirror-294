from functools import wraps
from .client import get_global_langfuse, get_global_callback_handler

def observe(**langfuse_kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            langfuse = get_global_langfuse()
            callback_handler = get_global_callback_handler()
            
            if langfuse is None or callback_handler is None:
                print("Warning: Langshark client or callback handler is not initialized. Skipping observation.")
                return func(*args, **kwargs)
            
            with callback_handler.as_span(**langfuse_kwargs) as span:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    span.end(error=str(e))
                    raise

        return wrapper
    return decorator