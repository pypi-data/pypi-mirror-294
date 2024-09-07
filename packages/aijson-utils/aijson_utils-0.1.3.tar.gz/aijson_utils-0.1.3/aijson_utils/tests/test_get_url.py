import pytest
from aijson_utils.actions.get_url import get_url


@pytest.mark.parametrize(
    "url, expected_text",
    (
        (
            "https://example.com",
            """Example Domain
This domain is for use in illustrative examples in documents. You may use this
    domain in literature without prior coordination or asking for permission.
More information...""",
        ),
    ),
)
async def test_get_url(url, expected_text):
    assert await get_url(url) == expected_text
