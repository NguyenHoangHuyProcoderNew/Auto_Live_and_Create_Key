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

"""" Trở lại menu chính """
def trolai_menuchinh(message):
    nut_menuchinh = telebot.types.ReplyKeyboardMarkup(True).add('Mở live', 'Tắt live', 'Đổi IP').add('Trở về menu chính')
    bot.send_message(message.chat.id, "VUI LÒNG CHỌN 👇", reply_markup=nut_menuchinh)

def main_test(message):
    driver = webdriver.Chrome(service=service, options=options)

    driver.get('https://autolive.me/tiktok')

    try:
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b')))
        print("Load trang web livestream thành công")

        dulieu_trangthai = driver.find_element(By.CSS_SELECTOR, "td.text-center:nth-child(10)").text

        if dulieu_trangthai == "Mới":
            print("Phiên live đã được mở")

    except TimeoutError:
        print("Load trang web thất bại")