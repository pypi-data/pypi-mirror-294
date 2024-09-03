from functools import wraps
from .client import get_global_langfuse, get_global_callback_handler

def observe(**langfuse_kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            langfuse = get_global_langfuse()
            if langfuse is None:
                print("Warning: Langshark client is not initialized. Skipping observation.")
                return func(*args, **kwargs)
            
            span = langfuse.span(**langfuse_kwargs)
            
            try:
                result = func(*args, **kwargs)
                span.end()
                return result
            except Exception as e:
                span.end(error=str(e))
                raise

        return wrapper
    return decorator