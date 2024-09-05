from malaysian_news_parser import get_parser
from config.publisher_config import PublisherConfigManager


# Initialize the PublisherConfigManager
config_manager = PublisherConfigManager()

# Example URL and publisher name
url = 'https://www.astroawani.com/berita-malaysia/pelajar-cemerlang-spm-dijamin-tempat-matrikulasi-atau-program-kpt-kpm-477101'
publisher_name = 'astro_awani'

# Get the parser for the publisher
parser = get_parser(publisher_name)

# Retrieve the article data
article_data = parser.get_article_data(url)

# Print the article data
if article_data:
    print(f"Title: {article_data['title']}")
    print(f"Author: {article_data['author']}")
    print(f"Date: {article_data['date']}")
    print(f"Body: {article_data['body'][:1000]}")  # Print the first 1000 characters to keep it concise
else:
    print("Failed to fetch or parse article data.")


def get_config(publisher_name):
    return config_manager.get_publisher_config(publisher_name)

def add_config(publisher_name, config):
    config_manager.add_publisher(publisher_name, config)

def update_config(publisher_name, updated_config):
    config_manager.update_publisher(publisher_name, updated_config)

def remove_config(publisher_name):
    config_manager.remove_publisher(publisher_name)


# Add a new publisher

def add_new_publisher():

    new_publisher_config = {
        'type': 'static',
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        },
        'body_selector': {
            'type': 'class',
            'element': 'div',
            'text': 'article-body'
        },
        'date_selector': {
            'type': 'class',
            'element': 'div',
            'text': 'article-date',
        },
        'author_selector': {
            'type': 'class',
            'element': 'div',
            'text': 'article-byline',
        }
    }

    add_config('new_publisher', new_publisher_config)

# Update an existing publisher
def update_existing_publisher():

    update_publisher_config = {
        "body_selector": {
            "type": "id",
            "element": "div",
            "text": "updated-body-selector"
        }
    }

    update_config('new_publisher', update_publisher_config)

def retrieve_publisher_config():
    
    config = get_config('new_publisher')

    if config:
        print(config)
    else:
        print("Publisher configuration not found.")

def remove_existing_publisher():
    remove_config('new_publisher')

add_new_publisher()
update_existing_publisher()
retrieve_publisher_config()
remove_existing_publisher()