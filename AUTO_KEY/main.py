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
from telebot import types

# Nhập moudles in log ra màn hình
from Moudles_support.print_log import log_info, log_warning, log_error, log_success

# Nhập moudles bot phản hồi lại người dùng
from Moudles_support.support_bot import bot_reply

# KHAI BÁO API TOKEN BOT TELEGRAM
API_TOKEN = '7371036517:AAEB8PtQRtSrvDOxQUUW2su7ObGso6ltq8w'  # TOKEN CỦA BOT
bot = telebot.TeleBot(API_TOKEN)

# BẮT ĐẦU CÁC CHỨC NĂNG CHÍHH CỦA BOT
log_success(f"KHỞI ĐỘNG BOT TẠO KEY THÀNH CÔNG - ĐANG CHỜ LỆNH TỪ NGƯỜI DÙNG...")

# Tạo key IOS server USER
@bot.message_handler(commands=['ios_user'])
def taokey_ios_user(message):
    from Moudles_key.ios_user import yeucau_nhap_thoigian_key_ios_user, xuly_taokey_ios_user

    yeucau_nhap_thoigian_key_ios_user(message)
    bot.register_next_step_handler(message, xuly_taokey_ios_user)

# Tạo key IOS server VIP
@bot.message_handler(commands=['ios_vip'])
def ios_vip(message):
    from Moudles_key.ios_vip import yeucau_nhap_thoigian_key_ios_vip, xuly_taokey_ios_vip

    yeucau_nhap_thoigian_key_ios_vip(message)
    bot.register_next_step_handler(message, xuly_taokey_ios_vip)

# Tạo key ANDROID
@bot.message_handler(commands=['android'])
def taokey_android(message):
    from Moudles_key.android import yeucau_nhap_thoigian_key_android, xuly_taokey_android

    yeucau_nhap_thoigian_key_android(message)
    bot.register_next_step_handler(message, xuly_taokey_android)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.exception("LỖI")
        time.sleep(5)