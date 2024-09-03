import functools
from .client import get_global_client

def observe():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            langfuse_client = get_global_client()
            span = langfuse_client.span(name=func.__name__)
            try:
                result = func(*args, **kwargs)
                span.end()
                return result
            except Exception as e:
                span.end(error=str(e))
                raise
        return wrapper
    return decorator