from aijson import register_action
import aiohttp
import bs4


@register_action
async def get_url(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            website_text = await response.text()

    soup = bs4.BeautifulSoup(website_text)
    if soup.body is None:
        raise ValueError("No body found on website")
    return soup.body.get_text(separator="\n", strip=True)
