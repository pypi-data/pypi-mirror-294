from functools import wraps
from typing import Optional, Literal, Callable, Any
from .client import get_global_langfuse
import asyncio

def observe(
    name: Optional[str] = None,
    as_type: Optional[Literal['generation']] = None,
    capture_input: bool = True,
    capture_output: bool = True,
    transform_to_string: Optional[Callable[[Any], str]] = None
):
    def decorator(func):
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            langfuse = get_global_langfuse()
            if langfuse is None:
                print("Warning: Langfuse client is not initialized. Skipping observation.")
                return func(*args, **kwargs)

            observation = langfuse.span(name=name or func.__name__)
            if as_type == "generation":
                observation = langfuse.generation(name=name or func.__name__)

            try:
                if capture_input:
                    observation.update(input={"args": args, "kwargs": kwargs})

                result = func(*args, **kwargs)

                if capture_output:
                    output = transform_to_string(result) if transform_to_string else result
                    observation.update(output=output)

                observation.end()
                return result
            except Exception as e:
                observation.end(error=str(e))
                raise

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            langfuse = get_global_langfuse()
            if langfuse is None:
                print("Warning: Langfuse client is not initialized. Skipping observation.")
                return await func(*args, **kwargs)

            observation = langfuse.span(name=name or func.__name__)
            if as_type == "generation":
                observation = langfuse.generation(name=name or func.__name__)

            try:
                if capture_input:
                    observation.update(input={"args": args, "kwargs": kwargs})

                result = await func(*args, **kwargs)

                if capture_output:
                    output = transform_to_string(result) if transform_to_string else result
                    observation.update(output=output)

                observation.end()
                return result
            except Exception as e:
                observation.end(error=str(e))
                raise

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator