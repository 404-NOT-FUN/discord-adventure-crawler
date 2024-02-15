from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
import time
import configparser
import os
import sys

def get_options():
    options = webdriver.EdgeOptions()

    options.set_capability("goog:loggingPrefs",{"performance": "ALL"})

    options.add_argument("--disable-animations")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-print-preview")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-site-isolation-trials")
    options.add_argument("--disable-smooth-scrolling")
    options.add_argument("--disable-sync")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-features=TranslateUI")
    options.add_argument("--disable-translate")
    options.add_argument("--disable-web-security")
    options.add_argument("--lang=zh-TW")
    options.add_argument("--incognito")
    options.add_argument("--inprivate")
    options.add_argument("--enable-chrome-browser-cloud-management")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False, 
        "profile.password_manager_enabled": False, 
        "translate":{"enabled": False}
    })
    options.add_experimental_option("detach", True)

    options.page_load_strategy = "eager"
    options.unhandled_prompt_behavior = "accept"

    return options

def get_config():
    config = configparser.ConfigParser()
    config_file = "config.ini"

    if not os.path.exists(config_file):
        print(rf"Config file {config_file} doesn't exist.")
        return None

    try:
        print(rf"Read config file : {config_file} .")
        config.read(config_file)
        return {"url": config.get("Setting", "url"), "wait_seconds": config.get("Setting", "wait_seconds")}
    except:
        print(rf"Fail to read config file {config_file}")
        return None
    
def main():
    config = get_config()
    if config is None:
        print("Fail to read config file")
        sys.exit(1)

    wait_seconds = config["wait_seconds"]

    driver = webdriver.Edge(
        service=Service(EdgeChromiumDriverManager(cache_manager=DriverCacheManager(r".\drivers")).install()),
        options=get_options())
    driver.implicitly_wait(wait_seconds)

    driver.get(config["url"])

    WebDriverWait(driver, wait_seconds).until(
        expected_conditions.presence_of_element_located((By.CLASS_NAME, "textArea__74543.textAreaSlate_e0e383.slateContainer_b692b3")))
    
    while True:
        builder = ActionChains(driver)
        builder.send_keys("/adventure ")
        builder.send_keys(Keys.ENTER)
        builder.perform()

        time.sleep(3)
        
        elements = driver.find_elements(By.CLASS_NAME, "component__43381.button_afdfd9.lookFilled__19298.colorGreen__5f181.sizeSmall__71a98.grow__4c8a4")
        for element in elements:
            if element.is_enabled():
                element.click()
                break

        time.sleep(40)

if __name__ == "__main__":
    main()