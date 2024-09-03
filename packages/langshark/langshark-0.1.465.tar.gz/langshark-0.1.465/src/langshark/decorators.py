# from functools import wraps
# from typing import Optional, Literal, Callable, Any
# from .client import get_global_langfuse
# import asyncio

# def observe(
#     name: Optional[str] = None,
#     as_type: Optional[Literal['generation']] = None,
#     capture_input: bool = True,
#     capture_output: bool = True,
#     transform_to_string: Optional[Callable[[Any], str]] = None
# ):
#     def decorator(func):
#         @wraps(func)
#         def sync_wrapper(*args, **kwargs):
#             langfuse = get_global_langfuse()
#             if langfuse is None:
#                 print("Warning: Langfuse client is not initialized. Skipping observation.")
#                 return func(*args, **kwargs)

#             observation = langfuse.span(name=name or func.__name__)
#             if as_type == "generation":
#                 observation = langfuse.generation(name=name or func.__name__)

#             try:
#                 if capture_input:
#                     observation.update(input={"args": args, "kwargs": kwargs})

#                 result = func(*args, **kwargs)

#                 if capture_output:
#                     output = transform_to_string(result) if transform_to_string else result
#                     observation.update(output=output)

#                 observation.end()
#                 return result
#             except Exception as e:
#                 observation.end(error=str(e))
#                 raise

#         @wraps(func)
#         async def async_wrapper(*args, **kwargs):
#             langfuse = get_global_langfuse()
#             if langfuse is None:
#                 print("Warning: Langfuse client is not initialized. Skipping observation.")
#                 return await func(*args, **kwargs)

#             observation = langfuse.span(name=name or func.__name__)
#             if as_type == "generation":
#                 observation = langfuse.generation(name=name or func.__name__)

#             try:
#                 if capture_input:
#                     observation.update(input={"args": args, "kwargs": kwargs})

#                 result = await func(*args, **kwargs)

#                 if capture_output:
#                     output = transform_to_string(result) if transform_to_string else result
#                     observation.update(output=output)

#                 observation.end()
#                 return result
#             except Exception as e:
#                 observation.end(error=str(e))
#                 raise

#         return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
#     return decorator

from functools import wraps
from typing import Optional, Literal, Callable, Any, List, Dict, Union
from .client import get_global_langfuse
import asyncio
import contextvars
from datetime import datetime

class LangfuseDecorator:
    def __init__(self):
        self._observation_stack = contextvars.ContextVar('observation_stack', default=[])

    def observe(self, name: Optional[str] = None, as_type: Optional[Literal['generation']] = None,
                capture_input: bool = True, capture_output: bool = True,
                transform_to_string: Optional[Callable[[Any], str]] = None):
        def decorator(func):
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                return self._run_observed(func, args, kwargs, name, as_type, capture_input, capture_output, transform_to_string)

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                return await self._run_observed_async(func, args, kwargs, name, as_type, capture_input, capture_output, transform_to_string)

            return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
        return decorator

    def _run_observed(self, func, args, kwargs, name, as_type, capture_input, capture_output, transform_to_string):
        langfuse = get_global_langfuse()
        if langfuse is None:
            print("Warning: Langfuse client is not initialized. Skipping observation.")
            return func(*args, **kwargs)

        observation = self._create_observation(langfuse, name or func.__name__, as_type)
        self._observation_stack.get().append(observation)

        try:
            if capture_input:
                observation.update(input={"args": args, "kwargs": kwargs})

            result = func(*args, **kwargs)

            if capture_output:
                output = transform_to_string(result) if transform_to_string else result
                observation.update(output=output)

            return result
        except Exception as e:
            observation.end(error=str(e))
            raise
        finally:
            observation.end()
            self._observation_stack.get().pop()

    async def _run_observed_async(self, func, args, kwargs, name, as_type, capture_input, capture_output, transform_to_string):
        langfuse = get_global_langfuse()
        if langfuse is None:
            print("Warning: Langfuse client is not initialized. Skipping observation.")
            return await func(*args, **kwargs)

        observation = self._create_observation(langfuse, name or func.__name__, as_type)
        self._observation_stack.get().append(observation)

        try:
            if capture_input:
                observation.update(input={"args": args, "kwargs": kwargs})

            result = await func(*args, **kwargs)

            if capture_output:
                output = transform_to_string(result) if transform_to_string else result
                observation.update(output=output)

            return result
        except Exception as e:
            observation.end(error=str(e))
            raise
        finally:
            observation.end()
            self._observation_stack.get().pop()

    def _create_observation(self, langfuse, name, as_type):
        return langfuse.generation(name=name) if as_type == "generation" else langfuse.span(name=name)

    def get_current_trace_id(self):
        stack = self._observation_stack.get()
        return stack[0].id if stack else None

    def get_current_trace_url(self):
        langfuse = get_global_langfuse()
        trace_id = self.get_current_trace_id()
        if langfuse and trace_id:
            return f"{langfuse.host}/traces/{trace_id}"
        return None

    def get_current_observation_id(self):
        stack = self._observation_stack.get()
        return stack[-1].id if stack else None

    def update_current_trace(self, **kwargs):
        stack = self._observation_stack.get()
        if stack:
            stack[0].update(**kwargs)
        else:
            print("Warning: No active trace found.")

    def update_current_observation(self, **kwargs):
        stack = self._observation_stack.get()
        if stack:
            stack[-1].update(**kwargs)
        else:
            print("Warning: No active observation found.")

    def score_current_observation(self, name: str, value: Union[float, str], **kwargs):
        stack = self._observation_stack.get()
        if stack:
            stack[-1].score(name=name, value=value, **kwargs)
        else:
            print("Warning: No active observation found.")

    def score_current_trace(self, name: str, value: Union[float, str], **kwargs):
        stack = self._observation_stack.get()
        if stack:
            stack[0].score(name=name, value=value, **kwargs)
        else:
            print("Warning: No active trace found.")

langfuse_context = LangfuseDecorator()
observe = langfuse_context.observe