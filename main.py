import time
import config
from linkedin_bot import LinkedInBot
from news_scraper import NewsScraper
from database import Database

def main():
    # Initialize database
    db = Database(config.DB_PATH)

    # Initialize LinkedIn bot
    linkedin_bot = LinkedInBot(config.LINKEDIN_EMAIL, config.LINKEDIN_PASSWORD)
    linkedin_bot.login()

    # Initialize news scraper
    news_scraper = NewsScraper(config.NEWS_SOURCES)

    while True:
        # Scrape news
        news_articles = news_scraper.scrape()

        # Store news in database
        db.store_news(news_articles)

        # Post news on LinkedIn
        for article in news_articles:
            linkedin_bot.post_update(article.title, article.url)

        # Connect with new people
        linkedin_bot.connect_with_people(config.SEARCH_KEYWORDS)

        # Wait for next cycle
        time.sleep(config.CYCLE_INTERVAL)

if __name__ == "__main__":
    main()