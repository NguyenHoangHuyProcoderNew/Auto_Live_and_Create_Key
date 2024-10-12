# IMPORT CÁC THƯ VIỆN CẦN THIẾT
import os
import time
import logging
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import telebot
import sys
from selenium.common.exceptions import NoSuchElementException
import datetime
from selenium.common.exceptions import TimeoutException
from colorama import Fore, Style, init
from telebot import types

# Cấu hình API telegram
API_TOKEN = '7329003333:AAF7GhjivbGnk0jSGE8XfefFh_-shHAFsGc' # Token của BOT
bot = telebot.TeleBot(API_TOKEN)

# Cấu hình Chrome driver
from Moudles_support.support_chrome_driver import chromedriver_path, dir
options = Options()
options.add_argument('--log-level=3')  # Vô hiệu hóa thông báo của Selenium
options.add_argument(f'--user-data-dir={dir}')

service = Service(chromedriver_path)
service_log_path = os.path.devnull
service = Service(chromedriver_path, service_log_path=service_log_path)

# Nhập chức năng in log ra màn hình
from Moudles_support.print_log import log_error, log_info, log_success

# Nhập chức năng bot phản hồi lại người dùng
from Moudles_support.support_bot import bot_reply

# ID của ADMIN Bot
from Moudles_support.support_bot import user_id

kieulive = None
"""" Trở lại menu chính """
def trolai_menuchinh(message):
    nut_menuchinh = telebot.types.ReplyKeyboardMarkup(True).add('Mở live', 'Tắt live', 'Đổi IP').add('Trở về menu chính')
    bot.send_message(message.chat.id, "VUI LÒNG CHỌN 👇", reply_markup=nut_menuchinh)

def chon_nguon(message):
    nut_chon_nguon_chophienlive = types.ReplyKeyboardMarkup(True).add('HC Cũ').add('Quỳnh Em').add('Trở lại menu chính')
    bot.send_message(message.chat.id, "Bạn muốn sử dụng nguồn live nào cho phiên live?", reply_markup=nut_chon_nguon_chophienlive)
    
    bot.register_next_step_handler(message, xuly_chonnguon)

def xuly_chonnguon(message):
    global linknguon
    if message.text == "HC Cũ":
        linknguon = "hoi chieu cu"
    elif message.text == "Quỳnh Em":
        linknguon = "quynhem_chui"
    elif message.text == "Trở lại menu chính":
        log_info(f"Người dùng đã chọn Trở lại menu chính")
        trolai_menuchinh(message)
        return
    else:
        bot_reply(user_id, "Lựa chọn không hợp lệ")
        trolai_menuchinh(message)
        log_error("Lựa chọn không hợp lệ - trở về menu chính")
        return
    
    # Sau khi chọn nguồn, chuyển sang bước chọn kiểu live
    chon_kieulive(message)

def chon_kieulive(message):
    nut_chon_kieulive = types.ReplyKeyboardMarkup(True).add('Kiểu live Mobile').add('Kiểu live Studio V3').add('Trở lại menu chính')
    bot.send_message(message.chat.id, "Bạn muốn sử dụng kiểu live nào cho phiên live?", reply_markup=nut_chon_kieulive)

    bot.register_next_step_handler(message, xuly_chonkieulive) 

def xuly_chonkieulive(message):
    global kieulive
    if message.text == "Kiểu live Mobile":
        kieulive = "#formLive > div:nth-child(6) > div > div > div > button.h-60.w-60.radius-6.btn-live-type.btn-icon.cur-point.m-r-15.pricing-box-active"
    elif message.text == "Kiểu live Studio V3":
        kieulive = "#live_studio_v3"
    elif message.text == "Trở lại menu chính":
        log_info(f"Người dùng đã chọn Trở lại menu chính")
        trolai_menuchinh(message)
        return
    else:
        bot_reply(user_id, "Lựa chọn không hợp lệ")
        trolai_menuchinh(message)
        return

    # Sau khi chọn kiểu live, thực hiện các thao tác tiếp theo
    bot_reply(user_id, f"Kiểu live: {kieulive}")
    bot_reply(user_id, f"Nguồn live: {linknguon}")
