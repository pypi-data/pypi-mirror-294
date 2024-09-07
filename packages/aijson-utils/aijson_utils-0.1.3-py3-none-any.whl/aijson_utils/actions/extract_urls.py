import re

from aijson import register_action

url_regex = r"(https?://[^\s,]+|www\.[^\s,]+|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"


@register_action
def extract_urls(text: str) -> list[str]:
    urls = re.findall(url_regex, text)
    # ensure they're all https://
    secure_urls = []
    for url in urls:
        url = url.replace("http://", "https://")
        if not url.startswith("http"):
            url = "https://" + url
        secure_urls.append(url)
    return secure_urls
