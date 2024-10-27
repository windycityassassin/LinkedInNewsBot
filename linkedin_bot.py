import requests
from bs4 import BeautifulSoup
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import config

class ContentScraper:
    def __init__(self, urls):
        self.urls = urls

    def scrape_articles(self):
        articles = []
        for url in self.urls:
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.find('h1').text.strip()
                content = ' '.join([p.text for p in soup.find_all('p')])
                articles.append({'title': title, 'content': content, 'url': url})
            except Exception as e:
                print(f"Error scraping {url}: {e}")
        return articles

    def select_best_article(self, articles):
        # This is a simple selection method. You might want to implement a more sophisticated one.
        return max(articles, key=lambda x: len(x['content']))

class LinkedInBot:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        
        brave_path = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
        options = Options()
        options.binary_location = brave_path
        
        service = Service(ChromeDriverManager().install())
        
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def login(self):
        print("Logging in to LinkedIn...")
        self.driver.get("https://www.linkedin.com/login")
        
        email_field = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        email_field.send_keys(self.email)
        
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys(self.password)
        password_field.submit()
        
        time.sleep(5)
        print("Login successful.")

    def create_post_content(self, article):
        title = article['title']
        summary = article['content'][:500] + "..."  # Truncate to 500 characters
        url = article['url']
        
        post_content = f"{title}\n\n"
        post_content += f"I recently read an interesting article and wanted to share my thoughts:\n\n"
        post_content += f"{summary}\n\n"
        post_content += f"What are your thoughts on this? Do you agree with the points made in the article?\n\n"
        post_content += f"Read more: {url}\n\n"
        post_content += "#TechNews #Innovation #ProfessionalDevelopment"
        
        return post_content

    def post_update(self, post_content):
        try:
            self.driver.get("https://www.linkedin.com/feed/")
            
            post_box = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "share-box-feed-entry__trigger")))
            post_box.click()
            
            post_textarea = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ql-editor")))
            post_textarea.send_keys(post_content)
            
            post_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "share-actions__primary-action")))
            post_button.click()
            
            time.sleep(random.uniform(3, 5))
            print("Posted update successfully.")
        except Exception as e:
            print(f"Error posting update: {e}")

    def close(self):
        self.driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    urls = [
        "https://www.techcrunch.com/",
        "https://www.wired.com/",
        "https://www.theverge.com/",
        # Add more URLs as needed
    ]
    
    scraper = ContentScraper(urls)
    articles = scraper.scrape_articles()
    best_article = scraper.select_best_article(articles)
    
    bot = LinkedInBot(config.LINKEDIN_EMAIL, config.LINKEDIN_PASSWORD)
    try:
        bot.login()
        post_content = bot.create_post_content(best_article)
        bot.post_update(post_content)
    finally:
        bot.close()