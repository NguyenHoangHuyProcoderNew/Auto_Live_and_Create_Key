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

def main_test(message):
    """"Nhập chức năng đóng toàn bộ trình duyệt Chrome trước khi khởi tạo Chrome driver mới"""
    from Moudles_support.support_chrome_driver import dong_toanbo_trinhduyet_chrome        

    """" Đóng các phiên trình duyệt Chrome cũ trước khi khởi tạo Chrome driver mới"""
    bot_reply(user_id, "Đóng các phiên trình duyệt Chrome cũ")
    log_info("Chạy hàm đóng toàn bộ trình duyệt trước khi khởi tạo Chrome driver mới")

    # Hàm đóng các phiên trình duyệt Chrome driver cũ
    dong_toanbo_trinhduyet_chrome(message)

    """" Xác nhận đã tắt các trình duyệt Chrome driver cũ thành công"""
    bot_reply(user_id, "Đóng các phiên trình duyệt Chrome cũ thành công")
    log_success("Chạy hàm đóng các phiên trình duyệt Chrome cũ hoàn tất")

    """" Khởi tạo Chrome driver mới"""
    bot_reply(user_id, "Khởi tạo trình duyệt Chrome driver mới")
    log_info("Khởi tạo chrome driver")
    driver = webdriver.Chrome(service=service, options=options)
    
    """" Truy cập vào trang web livestream """
    bot_reply(user_id, "Mở trang web live")
    log_info("Truy cập vào trang web live")

    driver.get('https://autolive.one/tiktok')

    # Kiểm tra xem có truy cập web livestream thành công hay không
    try:
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b')))

        bot_reply(user_id, "Mở trang web live thành công")
        log_success("Truy cập vào trang web live thành công")
    except TimeoutError:
        bot_reply(user_id, "Mở trang web thất bại, xảy ra sự cố kết nối internet")
        log_error("Truy cập vào trang web thất bại, xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt Chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return    
    
    try:
        # Đợi 1000 giây để dữ liệu của phần tử Trạng thái là "Mới"
        WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'td.text-center:nth-child(10)')))

        dulieu_trangthai = driver.find_element(By.CSS_SELECTOR, "td.text-center:nth-child(10)").text

        if "Đang" in dulieu_trangthai:

            bot_reply(user_id, "Hợp lệ")
            # bot_reply(user_id, f"Dữ liệu của phần tử trạng thái là {dulieu_trangthai}")
            # log_success(f"Dữ liệu của phần tử trạng thái là {dulieu_trangthai}")

            # driver.quit()
            # log_info("Đóng trình duyệt chrome")

            # log_info("Kết thúc tiến trình")
            # return            
    except TimeoutException:
        bot_reply(user_id, "Phần tử Trạng thái không chuyển sang dữ liệu mong muốn trong thời gian chờ, vui lòng kiểm tra lại kết nối internet")
        log_error("Không thành công, phần tử không xuất hiện trong thời gian chờ quy định")

        driver.quit()
        log_info("Đóng trình duyệt chrome")

        log_info("Kết thúc tiến trình")
        return