from .base_parser import BaseParser
from .parsers.static_parser import StaticParser
from .parsers.dynamic_parser import DynamicParser
from .config.publisher_config import PublisherConfigManager

config_manager = PublisherConfigManager()

def get_parser(publisher_name):
    config = config_manager.get_publisher_config(publisher_name)

    if not config:
        raise ValueError(f"Publisher {publisher_name} not found in the configuration.")
    
    if config['type'] == 'static':
        return StaticParser(config)
    elif config['type'] == 'dynamic':
        return DynamicParser(config)
    else:
        raise ValueError(f"Unsupported parser type {config['type']} for publisher {publisher_name}.")