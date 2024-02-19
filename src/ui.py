from tkinter import Tk, Entry, Checkbutton, Label, BooleanVar, Button
from tkinter.constants import CENTER
from threading import Thread
from src.utils import *
from src.crawler import *

class Threader(Thread):
    def __init__(self, config, inprivate_var, send_msg_var, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)
        self.config = config
        self.inprivate_var = inprivate_var
        self.send_msg_var = send_msg_var
        self.daemon = True
        self.start()
    def run(self):
        self.config["inprivate"] = self.inprivate_var.get()
        self.config["send_msg"] = self.send_msg_var.get()

        set_config(self.config)
        start_driver(self.config)

def main_window(config):
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

    execute = Button(text="執行", command=lambda: Threader(config=config, inprivate_var=inprivate_var, send_msg_var=send_msg_var, name="save_config_and_start_driver"))
    execute.place(x=200,y=130,anchor=CENTER)
    
    window.mainloop()