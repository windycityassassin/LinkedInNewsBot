import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass

@dataclass
class NewsArticle:
    title: str
    url: str
    source: str

class NewsScraper:
    def __init__(self, sources):
        self.sources = sources

    def scrape(self):
        articles = []
        for source in self.sources:
            articles.extend(self._scrape_source(source))
        return articles

    def _scrape_source(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []

        # This is a generic scraper. You might need to adjust selectors for each specific site.
        for article in soup.find_all('article'):
            title_elem = article.find('h2')
            link_elem = article.find('a')
            
            if title_elem and link_elem:
                title = title_elem.text.strip()
                link = link_elem['href']
                if not link.startswith('http'):
                    link = f"{url.rstrip('/')}/{link.lstrip('/')}"
                
                articles.append(NewsArticle(title=title, url=link, source=url))

        return articles