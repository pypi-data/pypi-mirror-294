import uuid
from langfuse import Langfuse
from langfuse.callback import CallbackHandler

DEFAULT_HOST = "https://langshark.fmops.kr"

class LangSharkClient:
    def __init__(self, secret_key, public_key, username, tracename, host=DEFAULT_HOST):
        self.secret_key = secret_key
        self.public_key = public_key
        self.host = host
        self.username = username
        self.session_uuid = str(uuid.uuid4())
        self.session_id = f"{username}_{self.session_uuid}"
        self.trace_name = f"{username}_{tracename}"

        self.langfuse = Langfuse(
            secret_key=secret_key,
            public_key=public_key,
            host=host,
        )

        self.callback_handler = CallbackHandler(
            secret_key=secret_key,
            public_key=public_key,
            host=host,
            trace_name=self.trace_name,
            session_id=self.session_id,
            user_id=username
        )

    def auth_check(self):
        return self.langfuse.auth_check() and self.callback_handler.langfuse.auth_check()

    def get_session_id(self):
        return self.session_id

def getLangShark(secret_key, public_key, username, tracename, host=DEFAULT_HOST):
    client = LangSharkClient(secret_key, public_key, username, tracename, host)
    return client.langfuse, client.callback_handler