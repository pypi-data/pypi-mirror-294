# import uuid
# from langfuse import Langfuse
# from langfuse.callback import CallbackHandler

# DEFAULT_HOST = "https://langshark.fmops.kr"
# global_langfuse_client = None

# class LangSharkClient:
#     def __init__(self, secret_key, public_key, username, tracename, host=DEFAULT_HOST):
#         self.secret_key = secret_key
#         self.public_key = public_key
#         self.host = host
#         self.username = username
#         self.session_uuid = str(uuid.uuid4())
#         self.session_id = f"{username}_{self.session_uuid}"
#         self.trace_name = f"{username}_{tracename}"

#         self.langfuse = Langfuse(
#             secret_key=secret_key,
#             public_key=public_key,
#             host=host,
#         )

#         self.callback_handler = CallbackHandler(
#             secret_key=secret_key,
#             public_key=public_key,
#             host=host,
#             trace_name=self.trace_name,
#             session_id=self.session_id,
#             user_id=username
#         )

#     def auth_check(self):
#         return self.langfuse.auth_check() and self.callback_handler.langfuse.auth_check()

#     def get_session_id(self):
#         return self.session_id

# def getLangShark(secret_key, public_key, username, tracename, host=DEFAULT_HOST):
#     global global_langfuse_client
#     client = LangSharkClient(secret_key, public_key, username, tracename, host)
#     global_langfuse_client = client.langfuse
#     return client.langfuse, client.callback_handler

# def get_global_client():
#     global global_langfuse_client
#     if global_langfuse_client is None:
#         raise ValueError("Langshark client not initialized. Call getLangShark first.")
#     return global_langfuse_client

from langfuse import Langfuse
from langfuse.callback import CallbackHandler

_global_langfuse_client = None
_global_callback_handler = None

def getLangShark(secret_key, public_key, username, tracename):
    global _global_langfuse_client, _global_callback_handler
    
    langfuse = Langfuse(secret_key=secret_key, public_key=public_key, host="https://langshark.fmops.kr")
    callback_handler = CallbackHandler(
        secret_key=secret_key,
        public_key=public_key,
        host="https://langshark.fmops.kr",
        trace_name=tracename,
        user_id=username
    )
    
    _global_langfuse_client = langfuse
    _global_callback_handler = callback_handler
    
    return langfuse, callback_handler

def get_global_langfuse():
    global _global_langfuse_client
    return _global_langfuse_client

def get_global_callback_handler():
    global _global_callback_handler
    return _global_callback_handler