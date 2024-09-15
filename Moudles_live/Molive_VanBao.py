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

# Trở lại menu chính
def trolai_menuchinh(message):
    nut_menuchinh = telebot.types.ReplyKeyboardMarkup(True).add('Mở live', 'Tắt live', 'Đổi IP').add('Trở về menu chính')
    bot.send_message(message.chat.id, "VUI LÒNG CHỌN 👇", reply_markup=nut_menuchinh)

# Yêu cầu người dùng chọn nguồn cho phiên live 
def chon_nguon_chophienlive_vanbao(message):
    # Tạo nút chọn nguồn cho phiên live
    nut_chon_nguon_chophienlive = types.ReplyKeyboardMarkup(True).add('Hồi Chiêu', 'Quỳnh Em', 'Nam Mod').add('Trở lại menu chính')
    bot.send_message(message.chat.id, "Bạn muốn sử dụng nguồn live nào cho phiên live?", reply_markup=nut_chon_nguon_chophienlive)
    log_info("Đang yêu cầu người dùng chọn nguồn cho phiên live")
    
    bot.register_next_step_handler(message, xuly_molive_vanbao)

# Xử lý việc mở live
def xuly_molive_vanbao(message):
    # Nhập hàm đóng trình duyệt Chrome driver cũ
    from Moudles_support.support_chrome_driver import dong_chromedriver_cu
    from Moudles_support.support_bot import id_tiktok_vanbao, chon_taikhoan_vanbao, hoichieu_fullhd, quynhem, nammod

    id_tiktok = "vanbao165201"
    chon_taikhoan_taocauhinhmoi = "#tiktok_account > option:nth-child(6)"

    # Kiểm tra sự lựa chọn mà người dùng đã chọn ở hàm Chọn Nguồn Cho Phiên Live
    if message.text == "Hồi Chiêu":
        bot_reply(user_id, "Tiến hành mở phiên live với nguồn HỒI CHIÊU")
        log_info(f"Người dùng đã chọn nguồn live HỒI CHIÊU")

        bot_reply(user_id, "Truy cập vào trang web livestream")
        linknguon = hoichieu_fullhd
    elif message.text == "Quỳnh Em":
        bot_reply(user_id, "Tiến hành mở phiên live với nguồn QUỲNH EM")
        log_info("Tiến hành mở phiên live với nguồn QUỲNH EM")

        bot_reply(user_id, "Truy cập vào trang web livestream")
        linknguon = quynhem
    elif message.text == "Nam Mod":
        bot_reply(user_id, "Tiến hành mở phiên live với nguồn Nam Mod")
        log_info("Người dùng đã chọn nguồn live Nam Mod")

        bot_reply(user_id, "Truy cập vào trang web livestream")
        linknguon = nammod
    elif message.text == "Trở lại menu chính":
        log_info(f"Người dùng đã chọn Trở lại menu chính")
        trolai_menuchinh(message)
        return
    else:
        bot_reply(user_id, "Lựa chọn không hợp lệ")
        trolai_menuchinh(message)
        log_error("Lựa chọn không hợp lệ - trở về menu chính")
        return
    
    # Gọi chức năng đóng trình duyệt Chrome driver cũ
    bot_reply(user_id, "Đóng các phiên trình duyệt Chrome driver cũ")
    log_info("Chạy hàm đóng các phiên trình duyệt Chrome driver cũ")

    dong_chromedriver_cu(message) # Chạy hàm đóng các phiên trình duyệt Chrome driver cũ

    # Khởi tạo Chrome driver
    driver = webdriver.Chrome(service=service, options=options)

    # Mở trang web livestream
    try:
        driver.get("https://autolive.me/tiktok")

        # Chờ element xuất hiện để xác định có truy cập trang web livestream thành công hay khong
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b'))
        )

        bot_reply(user_id, "Truy cập trang web livestream thành công")

    except TimeoutError:
