# LangShark

LangShark is a wrapper for Langfuse with enhanced functionality, designed to simplify the process of creating Langfuse clients and callback handlers.

## Installation

```bash
pip install langshark

## Usage
```python
from langshark import getLangShark

secret_key = "your_secret_key"
public_key = "your_public_key"
username = "YourUsername"
tracename = "your_tracename"

# 기본 host 사용 (https://langshark.fmops.kr)
langshark_client, langshark_handler = getLangShark(secret_key, public_key, username, tracename)

# 또는 사용자 지정 host 사용
custom_host = "https://your-custom-host.com"
langshark_client, langshark_handler = getLangShark(secret_key, public_key, username, tracename, custom_host)

# Use langshark_client and langshark_handler as needed
assert langshark_client.auth_check()
assert langshark_handler.langfuse.auth_check()

print(f"Session ID: {langshark_handler.session_id}")
print(f"Trace Name: {langshark_handler.trace_name}")
```

##License
This project is licensed under the MIT License - see the LICENSE file for details.
