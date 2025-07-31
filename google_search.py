import asyncio
import aiohttp
from googlesearch import search
from bs4 import BeautifulSoup
import time

async def fetch_url(session, url):
    """Fetch and summarize content from a URL asynchronously."""
    try:
        async with session.get(url, timeout=10) as resp:
            resp.raise_for_status()
            html = await resp.text()
            soup = BeautifulSoup(html, 'html.parser')
            text = ' '.join(p.text for p in soup.find_all('p'))
            return text[:10000]
    except Exception as e:
        return ''

async def search_and_fetch(query, num_results=5):
    """Search Google and concurrently fetch and summarize results."""
    start = time.time()

    # Run Google search in a thread (since it's blocking)
    loop = asyncio.get_running_loop()
    urls = await loop.run_in_executor(None, lambda: list(search(query, num_results=num_results)))

    # Fetch all URLs concurrently
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=10)) as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

    return results

# Main runner
if __name__ == "__main__":
    async def main():
        start = time.perf_counter()
        query = "Who won IPL match in 2025"
        print(f"Searching for: {query}")
        results = await search_and_fetch(query)
        end = time.perf_counter()
        print("\n" + "="*50 + "\nRESULTS:\n" + "="*50, "\nProcessing Time = ", end-start, "\n")
        print(results)

    asyncio.run(main())
