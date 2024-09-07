import pytest

from aijson_utils.actions.extract_urls import extract_urls


@pytest.mark.parametrize("text, expected", [
    ("https://www.google.com", ["https://www.google.com"]),
    ("https://www.google.com, https://www.facebook.com", ["https://www.google.com", "https://www.facebook.com"]),
    ("https://www.google.com\nhttps://www.facebook.com", ["https://www.google.com", "https://www.facebook.com"]),
    ("https://www.google.com https://www.facebook.com", ["https://www.google.com", "https://www.facebook.com"]),
    ("https://www.google.com - https://www.facebook.com", ["https://www.google.com", "https://www.facebook.com"]),
    ("https://www.google.com, https://www.facebook.com\nhttps://www.twitter.com - https://www.instagram.com", ["https://www.google.com", "https://www.facebook.com", "https://www.twitter.com", "https://www.instagram.com"]),
    ("google.com", ["https://google.com"]),
    ("www.google.com", ["https://www.google.com"]),
    ("google.com, www.facebook.com", ["https://google.com", "https://www.facebook.com"]),
    ("http://google.com", ["https://google.com"]),
])
def test_extract_urls(text, expected):
    assert extract_urls(text) == expected
