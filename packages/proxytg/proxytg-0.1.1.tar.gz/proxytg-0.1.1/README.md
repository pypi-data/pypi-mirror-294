## proxytg
This package implements TelegramAccount class, which can be used for automating tasks on telegram
with proxy(uses https://mobileproxy.space api).
## Usage
```python
from proxytg.telegram import TelegramAccount

proxy_data = {
    "key": "proxy_key_from_mobile_proxy",
    "authorization": "mobile_proxy_api_authorization"
}
obj = TelegramAccount("account_name", proxy_data, "path_to_sessions_dir")

```
if object with given account_name already exist in sessions directory, then cookies and local storage would
be loaded(to keep telegram session persistent)