import os
from dotenv import load_dotenv

load_dotenv()

class PublisherConfigManager:
    def __init__(self):
        self.publisher_configs = {
            "astro_awani": {
                "type": "dynamic",
                "chrome_path": os.getenv('CHROME_PATH'),
                "body_selector": {
                    "type": "class",
                    "element": "article",
                    "text": "styledComponents__ArticleContent-sc-1ym9iti-12"
                },
                "date_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "styledComponents__ArticleDate-sc-1ym9iti-8",
                },
                "author_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "styledComponents__Author-sc-1ym9iti-7"
                },
                "sleep_time": 10,
            },
            "malay_mail": {
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "article-body",
                },
                "date_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "article-date"
                },
                "author_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "article-byline"
                },
            },
            "star": {
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "id",
                    "element": "div",
                    "text": "story-body"
                },
                "date_selector": {
                    "type": "class",
                    "element": "p",
                    "text": "date",
                }
            },
            "sun_daily": {
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "paragraph"
                },
                "date_selector": {
                    "type": "class",
                    "element": "li",
                    "text": "date"
                }
            },
            "fmt": {
                "type": "dynamic",
                "chrome_path": os.getenv('CHROME_PATH'),
                "body_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "news-content"
                },
                "date_selector": {
                    "type": "class",
                    "element": "time",
                    "text": "text-sm text-blue-600",
                },
                "author_selector": {
                    "type": "css",
                    "text": "body > div:nth-of-type(5) > div:nth-of-type(2) > main > article > header > div > a > span",
                },
                "sleep_time": 5,
            },
            "sinar_harian": {
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "id",
                    "element": "div",
                    "text": "articleText",
                },
                "date_selector": {
                    "type": "class",
                    "element": "span",
                    "text": "timespan",
                },
                "author_selector": {
                    "type": "class",
                    "element": "a",
                    "text": "authorName",
                },
            },
            "berita_harian": {
                "type": "dynamic",
                "chrome_path": os.getenv('CHROME_PATH'),
                "body_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "article-content"
                },
                "date_selector": {
                    "type": "css",
                    "text": "body > div:nth-of-type(1) > main > div > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > div > div > div:nth-of-type(1) > div:nth-of-type(1) > div",
                },
                "author_selector": {
                    "type": "css",
                    "text": "body > div:nth-of-type(1) > main > div > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > div > div > div:nth-of-type(1) > div:nth-of-type(1) > div > span > a",
                },
                "sleep_time": 5,
            },
            "roti_kaya": {
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "class",
                    "element": "article",
                    "text": "the-content",
                },
                "date_selector": {
                    "type": "css",
                    "text": "body > main > section > div > div > div > section > div:nth-of-type(2)",
                },
                "author_selector": {
                    "type": "css",
                    "text": "body > main > section > div > div > div > section > div:nth-of-type(1) > strong",
                },
            },
            "nst": {
                "type": "dynamic",
                "chrome_path": os.getenv('CHROME_PATH'),
                "body_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "article-content",
                },
                "date_selector": {
                    "type": "css",
                    "text": "body > div:nth-of-type(1) > main > div > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > div > div > div:nth-of-type(1) > div:nth-of-type(1) > div",
                },
                "author_selector": {
                    "type": "css",
                    "text": "body > div:nth-of-type(1) > main > div > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > div > div > div:nth-of-type(1) > div:nth-of-type(1) > div > span > a",
                },
                "sleep_time": 5,
            },
            "the_vibes": {
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "body",
                },
                "date_selector": {
                    "type": "css",
                    "text": "body > section > div:nth-of-type(1) > div > div > p:nth-of-type(2)",
                },
                "author_selector": {
                    "type": "css",
                    "text": "body > section > div:nth-of-type(1) > div > div > p:nth-of-type(1)",
                },
            },
            "world_of_buzz": {
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "id",
                    "element": "div",
                    "text": "mvp-content-main",
                },
                "date_selector": {
                    "type": "css",
                    "text": "#mvp-post-head > div > div.mvp-author-info-text.left.relative > div.mvp-author-info-date.left.relative > span.mvp-post-date.updated > time",
                },
                "author_selector": {
                    "type": "css",
                    "text": "#mvp-post-head > div > div.mvp-author-info-text.left.relative > div.mvp-author-info-name.left.relative > span > a",
                }
            },
            "bernama": {
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "css",
                    "text": "#body-row > div > div.container.px-0.my-0 > div > div.col-12.col-sm-12.col-md-12.col-lg-8",
                },
                "date_selector": {
                    "type": "css",
                    "text": "#body-row > div > div.container.px-0.my-0 > div > div.col-12.col-sm-12.col-md-12.col-lg-8 > div.col-12.mt-3.mb-3 > div"
                }
            },
            "cili_sos": {
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "entry-content",
                },
                "date_selector": {
                    "type": "class",
                    "element": "span",
                    "text": "entry-meta-date"
                },
                "author_selector": {
                    "type": "class",
                    "element": "span",
                    "text": "author"
                }
            },
            "coconuts": {
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "coco_post-content",
                },
                "date_selector": {
                    "type": "class",
                    "element": "span",
                    "text": "post-timeago",
                },
                "author_selector": {
                    "type": "css",
                    "text": "#main-content > div > main > div.post-sheet > div.section-wrap > div > div > div.col-md-8.col-content.main-stream-content.pos-relative > div.coco_post-meta.d-md-flex.justify-content-between.align-items-center > div > span > a",
                },
            },
            "the_edge": {
                "type": "dynamic",
                "chrome_path": os.getenv('CHROME_PATH'),
                "body_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "news-detail_newsTextDataWrap__PkAu5",
                },
                "date_selector": {
                    "type": "css",
                    "text": "#__next > div > div > div > div > div.news-detail_articleContainerWrapper__pE31f > div:nth-child(1) > div > div.news-detail_pageWrapperContent__QWIfQ > div > div.news-detail_newsdetailsContent__Fey_B > div.news-detail_newsDetailsItemWrap___HS1t > div.news-detail_newsdetailsItemInfo__g9Hsi > div.news-detail_newsInfo__dv0be > span",
                },
                "sleep_time": 5,
            },
            "hmetro": {
                "type": "dynamic",
                "chrome_path": os.getenv('CHROME_PATH'),
                "body_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "article-content"
                },
                "date_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "published-date"
                },
                "author_selector": {
                    "type": "css",
                    "text": "#main > div > div.row > div.col > div:nth-child(1) > div > div > div.d-block.d-lg-flex.mb-3 > div.article-meta.mb-2.mb-lg-0.d-flex.align-items-center > div > span > a",
                },
            },
            "malaysia_gazette": {
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "td-post-content"
                },
                "date_selector": {
                    "type": "class",
                    "element": "time",
                    "text": "entry-date updated td-module-date"
                },
                "author_selector": {
                    "type": "class",
                    "element": "span",
                    "text": "td-post-author-name"
                },
            },
            "harakah_daily": {
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "td-post-content"
                },
                "date_selector": {
                    "type": "class",
                    "element": "time",
                    "text": "entry-date updated td-module-date"
                },
            },
            "borneo_post": {
                "type": "static",
                "headers": {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    # 'Accept-Language': 'en-US,en;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate, br',
                    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    # 'Connection': 'keep-alive',
                    # 'Upgrade-Insecure-Requests': '1',
                },
                "body_selector": {
                    "type": "class",
                    "element": "div",
                    "text": "post-content"
                },
                "date_selector": {
                    "type": "class",
                    "element": "time",
                    "text": "value-title"
                },
                "author_selector": {
                    "type": "class",
                    "element": "span",
                    "text": "reviewer"
                },
            }
            
        }


    def add_publisher(self, name, config):
        '''
            Adds a new publisher configuration.

            Parameters:
                name (str): The name of the publisher.
                config (dict): The configuration for the publisher.
        '''

        # Add the new publisher configuration
        if name in self.publisher_configs:
            raise ValueError(f"Publisher with name '{name}' already exists.")
        
        #print(self.publisher_configs[name])
        self.publisher_configs[name] = config

    def update_publisher(self, name, config):
        '''
            Updates an existing publisher configuration

            Parameters:
                name (str): The name of the publisher.
                config (dict): The new configuration for the publisher.
        '''

        # Update the publisher configuration
        if name not in self.publisher_configs:
            raise ValueError(f"Publisher with name '{name}' does not exist.")
        
        self.publisher_configs[name].update(config)

    def remove_publisher(self, name):
        '''
            Removes a publisher configuration.

            Parameters:
                name (str): The name of the publisher.
        '''

        # Remove the publisher configuration
        if name not in self.publisher_configs:
            raise ValueError(f"Publisher with name '{name}' does not exist.")
        
        del self.publisher_configs[name]

    def get_publisher_config(self, name):
        '''
            Returns the configuration for the specified publisher.

            Parameters:
                name (str): The name of the publisher.

            Returns:
                dict: The configuration for the specified publisher.
        '''

        # Get the publisher configuration
        if name not in self.publisher_configs:
            raise ValueError(f"Publisher with name '{name}' does not exist.")
        
        return self.publisher_configs[name]

