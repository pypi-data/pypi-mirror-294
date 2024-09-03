from functools import wraps
from .client import get_global_client, global_langfuse_client

def observe(**langfuse_kwargs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # global_langfuse_client는 Langfuse 인스턴스입니다
            # callback_handler는 getLangShark에서 별도로 반환됩니다
            
            # 여기서는 span 메서드를 직접 사용합니다
            span = global_langfuse_client.span(**langfuse_kwargs)
            
            try:
                # Execute the function
                result = func(*args, **kwargs)
                span.end()  # 성공적으로 종료
                return result
            except Exception as e:
                span.end(error=str(e))  # 에러와 함께 종료
                raise

        return wrapper
    return decorator