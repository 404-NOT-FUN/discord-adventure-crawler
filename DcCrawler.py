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
import threading
import os
from json import load, dump
from sys import exit
from tkinter import Tk, Entry, Checkbutton, Label, BooleanVar, Button
from tkinter.constants import CENTER

def get_options(config):
    options = webdriver.EdgeOptions()

    options.set_capability("goog:loggingPrefs",{"performance": "ALL"})

    user_data_dir = os.path.abspath(os.path.join("..", "discord-adventure-crawler", "drivers", "driver_data"))
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

def get_config():
    config_file = "config.json"

    if not os.path.exists(config_file):
        print(rf"Config file {config_file} doesn't exist.")
        return None

    try:
        print(rf"Read config file : {config_file} .")
        with open(config_file, "r", encoding="utf-8") as f:
            return load(f)
        
    except:
        print(rf"Fail to read config file {config_file}")
        return None
    
def send_adventure_request(builder):
    while True:
        logged_time = time.strftime("%H:%M:%S", time.localtime())
        try:
            builder.send_keys("/adventure ")
            builder.send_keys(Keys.ENTER)
            builder.perform()

            print(f"{logged_time}, thread_send_adventure_request sending success")
    
        except:
            print(f"{logged_time}, thread_send_adventure_request failed")

        finally:
            time.sleep(60)

def scroll_and_wait_for_element(driver):
    while True:
        logged_time = time.strftime("%H:%M:%S", time.localtime())
        # 将页面滚动到底部
        driver.execute_script("window.scroll(0, document.body.scrollHeight);")
        time.sleep(2)

        element_found = False
        elements = driver.find_elements(By.CLASS_NAME, "component__43381.button_afdfd9.lookFilled__19298.colorGreen__5f181.sizeSmall__71a98.grow__4c8a4")
        for element in elements:
            if element.is_enabled():
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(2)
                element.click()
                print(f"thread_scroll_and_wait_for_element 找到並點擊參加。")
                element_found = True
                break
                    
        # 根据是否找到元素决定等待时间
        if element_found:
            print(f"{logged_time}, thread_scroll_and_wait_for_element 成功，等待120秒。")
            time.sleep(120)
        else:
            print(f"{logged_time}, thread_scroll_and_wait_for_element 失敗，20秒後重試。")
            time.sleep(20)
    
def set_config(config):
    with open("config.json", "w", encoding="utf-8") as f:
        dump(config, f, indent=4)

"""
def send_adventure(driver):
    builder = ActionChains(driver)
    builder.send_keys("/adventure ")
    builder.send_keys(Keys.ENTER)
    builder.perform()

def click_join(driver):
    elements = driver.find_elements(By.CLASS_NAME, "component__43381.button_afdfd9.lookFilled__19298.colorGreen__5f181.sizeSmall__71a98.grow__4c8a4")
    for element in elements:
        if element.is_enabled():
            element.click()
            break
"""

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
        if config["send_msg"]:
            thread_send_adventure_request = threading.Thread(target=send_adventure_request, args=(builder, ))
            thread_send_adventure_request.start()
        
        thread_scroll_and_wait_for_element = threading.Thread(target=scroll_and_wait_for_element, args=(driver, ))
        thread_scroll_and_wait_for_element.start()

    except:
        print("Error to crawler.")
        return

def validate_int(user_input):
    if str.isdigit(user_input) or user_input == "":
        return True
    else:
        return False

class Threader(threading.Thread):
    def __init__(self, config, inprivate_var, send_msg_var, period_second, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.config = config
        self.inprivate_var = inprivate_var
        self.send_msg_var = send_msg_var
        self.period_second = period_second
        self.daemon = True
        self.start()
    def run(self):
        self.config["inprivate"] = self.inprivate_var.get()
        self.config["send_msg"] = self.send_msg_var.get()
        self.config["period_second"] = int(self.period_second.get())

        set_config(self.config)
        start_driver(self.config)


if __name__ == "__main__":
    config = get_config()
    
    if config is None:
        print("Fail to read config file")
        exit(1)

    window = Tk()
    window.title("Discord Adventure Crawler")
    window.geometry("400x200")
    window.resizable(False, False)

    url_label = Label(text="頻道URL:")
    url_label.place(x=50,y=40,anchor=CENTER)
    url = Entry(width=40)
    url.place(x=230,y=40,anchor=CENTER)
    url.insert(0, config["url"])
    
    inprivate_var = BooleanVar()
    inprivate = Checkbutton(text="啟用無痕",state="normal", variable=inprivate_var)
    inprivate.place(x=200,y=60,anchor=CENTER)
    inprivate.select() if config["inprivate"] else inprivate.deselect()

    send_msg_var = BooleanVar()
    send_msg = Checkbutton(text="定時送出指令",state="normal", variable=send_msg_var)
    send_msg.place(x=200,y=80,anchor=CENTER)
    send_msg.select() if config["send_msg"] else send_msg.deselect()

    period = Label(text="間隔秒數:")
    period.place(x=165,y=100,anchor=CENTER)
    valid = (window.register(validate_int), "%P")
    period_second = Entry(validate="key", validatecommand=valid, width=6)
    period_second.place(x=225,y=100,anchor=CENTER)
    period_second.insert(0, config["period_second"])

    execute = Button(text="執行", command=lambda: Threader(config=config, inprivate_var=inprivate_var, send_msg_var=send_msg_var, period_second=period_second, name="save_config_and_start_driver"))
    execute.place(x=200,y=130,anchor=CENTER)
    
    window.mainloop()