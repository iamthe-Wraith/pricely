import requests
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self):
        pass

    def crawl(self, url: str) -> float | None:
        try:
            html = self._load_page(url)

            if (html is None):
                return None

            soup = BeautifulSoup(html, "html.parser")

            titleElement = soup.select_one("#productTitle")
            title = titleElement.text.strip()

            dollarsElement = soup.select_one(".a-price-whole")
            dollars = dollarsElement.text.replace(".", "").strip()
            centsElement = soup.select_one(".a-price-fraction")
            cents = centsElement.text.strip()

            price = float(f"{dollars}.{cents}")

            return {
                "title": title,
                "price": price
            }
        except Exception as e:
            print(f"Error crawling page: {e}")
            print(f"URL: {url}")

            return None

    def _load_page(self, url: str) -> str | None:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "Accept-Language": "en-US",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
            }

            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error loading page: {e}")
            return None
