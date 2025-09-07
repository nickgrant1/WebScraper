# WebScraper

Run "main.py" with url of website you want to scrape, takes optional arguments of "max_concurrency" and "max_pages" in that order. Only traverses urls in the same domain. Returns a ".csv" spreadsheet showing each pages' first header, first paragraph, outgoing link urls, and image urls.

## Requirements

- Python 3.10+
- beautifulsoup4 version 4.13.4 (an easy-to-use webscraper library)
- aiohttp version 3.12.12 (an async http client library)
- requests version 2.32.4 (a simple http library)

```
uv add beautifulsoup4==4.13.4
uv add aiohttp==3.12.12
uv add requests==2.32.4
```
