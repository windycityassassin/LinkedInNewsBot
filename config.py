# LinkedIn credentials
LINKEDIN_EMAIL = "ogtrailblazer@icloud.com"
LINKEDIN_PASSWORD = "PrithviVadla123!@#"

# Database configuration
DB_PATH = "networking_bot.db"

# News sources to scrape
NEWS_SOURCES = [
    "https://www.techcrunch.com/category/enterprise/",
    "https://www.zdnet.com/topic/networking/",
    "https://www.networkworld.com/"
]

# Keywords for LinkedIn search
SEARCH_KEYWORDS = ["networking", "SDN", "NFV", "5G", "cybersecurity"]

# Time interval between cycles (in seconds)
CYCLE_INTERVAL = 3600  # 1 hour

# LinkedIn automation settings
MAX_CONNECTIONS_PER_DAY = 25
MAX_POSTS_PER_DAY = 3

# Personalized connection message
CONNECTION_MESSAGE = "Hi {first_name}, I noticed we're both in the networking industry. I'd love to connect and share insights!"