import sys
import logging
from colorlog import ColoredFormatter

from src.ui import *

logger = logging.getLogger(__name__)

def setup_logging():
    formatter = ColoredFormatter(
        '%(asctime)s %(log_color)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'white',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(
        filename="crawler.log", encoding="utf-8", mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logging.basicConfig(
        handlers=[stream_handler, file_handler], level=logging.INFO
    )

def main():
    setup_logging()
    config = get_config()
    
    if config is None:
        logger.error("Fail to read config file.")
        sys.exit(1)

    config["version"] = "2024.02.20"
    main_window(config)

if __name__ == "__main__":
    main()