import os
import logging
import shutil
import json

logger = logging.getLogger("__main__")

def get_config():
    config_file = "config.json"

    if not os.path.exists(config_file):
        example_config_file = "config.example.json"
        try:
            logger.info(f"Create {config_file} from {example_config_file}.")
            shutil.copyfile(example_config_file, config_file)
        except:
            logger.error(f"Failed to create {config_file}, due to {example_config_file} does't exist.")
            return None

    try:
        logger.info(f"Read config file: {config_file}.")
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        logger.error(rf"Failed to read config file: {config_file}")
        return None
    
def set_config(config):
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)