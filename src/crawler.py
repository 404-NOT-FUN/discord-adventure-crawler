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
from threading import Thread
import os
import logging

logger = logging.getLogger("__main__")

def get_options(config):
    options = webdriver.EdgeOptions()

    options.set_capability("goog:loggingPrefs",{"performance": "ALL"})

    user_data_dir = os.path.abspath(os.path.join("drivers", "driver_data"))

    options.add_argument(f"user-data-dir={user_data_dir}")
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

    if config["inprivate"]:
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
    
def send_adventure_request(builder):
    while True:
        try:
            builder.send_keys("/adventure ")
            builder.send_keys(Keys.ENTER)
            builder.perform()

            logger.info("thread_send_adventure_request sending success")
    
        except:
            logger.info("thread_send_adventure_request failed")

        finally:
            time.sleep(60)

def scroll_and_wait_for_element(driver):
    while True:
        # 將頁面滾動至底部
        driver.execute_script("window.scroll(0, document.body.scrollHeight);")
        time.sleep(2)

        element_found = False
        try:
            elements = driver.find_elements(By.CLASS_NAME, "component__43381.button_afdfd9.lookFilled__19298.colorGreen__5f181.sizeSmall__71a98.grow__4c8a4")
            for element in elements:
                if element.is_enabled():
                    driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    time.sleep(2)
                    element.click()
                    logger.info("thread_scroll_and_wait_for_element 找到並點擊參加。")
                    element_found = True
                    break
        except:
            logger.info("thread_scroll_and_wait_for_element error finding button。")
                    
        finally:
            # 根據是否找到元件決定等待時間
            if element_found:
                logger.info("thread_scroll_and_wait_for_element 成功，等待120秒。")
                time.sleep(120)
            else:
                logger.warning("thread_scroll_and_wait_for_element 失敗，20秒後重試。")
                time.sleep(20)

def start_driver(config):
    wait_seconds = config["wait_seconds"]

    driver = webdriver.Edge(
        service=Service(EdgeChromiumDriverManager(cache_manager=DriverCacheManager(r".\drivers")).install()),
        options=get_options(config))
    driver.implicitly_wait(wait_seconds)

    try:
        for _ in range(config["retry"]):
            try:
                driver.get(config["url"])

                WebDriverWait(driver, wait_seconds).until(
                    expected_conditions.presence_of_element_located((By.CLASS_NAME, "textArea__74543.textAreaSlate_e0e383.slateContainer_b692b3")))
            except:
                if _ < config["retry"]:
                    driver.refresh()
                else:
                    raise
            else:
                break

        builder = ActionChains(driver)
        builder_send_start_msg(config, builder)
        time.sleep(2)

        if config["send_msg"]:
            thread_send_adventure_request = Thread(target=send_adventure_request, args=(builder, ))
            thread_send_adventure_request.start()
        
        thread_scroll_and_wait_for_element = Thread(target=scroll_and_wait_for_element, args=(driver, ))
        thread_scroll_and_wait_for_element.start()

    except:
        logger.error("Error to crawler.")
        return

def builder_send_start_msg(config, builder):
    builder.send_keys(f"> **Discord Adventure Crawler v{config['version']}** | **[取得最新版本](https://github.com/404-NOT-FUN/discord-adventure-crawler/releases/latest)** | **[Discord 支援伺服器](https://discord.gg/XXn5udJsPU)**")
    builder.send_keys(Keys.ENTER)
    builder.perform()