import aiohttp
from bs4 import BeautifulSoup
import asyncio

async def get_page_content(url: str) -> str:
    """Fetch and parse webpage content."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "TE": "Trailers",
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            # Add timeout to prevent hanging
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Remove unwanted elements
                    for element in soup(['script', 'style', 'header', 'footer', 'nav']):
                        element.decompose()
                    
                    # Look for common lyrics container classes/IDs
                    lyrics_containers = soup.select(
                        '.lyrics, #lyrics, .lyricbox, .song-text, '
                        '.verse, [class*="lyrics"], [id*="lyrics"]'
                    )
                    
                    if lyrics_containers:
                        # Use the first container that has significant text
                        for container in lyrics_containers:
                            text = container.get_text(strip=True)
                            if len(text) > 100:  # Minimum length to be considered lyrics
                                return text
                    
                    # Fallback to main content if no lyrics container found
                    main_content = soup.select_one('main, article, .content, #content')
                    if main_content:
                        return main_content.get_text(strip=True)
                    
                    # Last resort: return all text
                    return soup.get_text(strip=True)
                else:
                    return ""
        except asyncio.TimeoutError:
            return ""
        except Exception as e:
            return ""