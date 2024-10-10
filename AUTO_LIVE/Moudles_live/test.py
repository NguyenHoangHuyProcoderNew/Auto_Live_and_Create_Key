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
    driver = webdriver.Chrome(service=service, options=options)

    # driver.get('https://www.tiktok.com/@phuoc19903/live')

# Kiểm tra xem có truy cập phiên live thành công hay không lần 1
    try:
        # Mở trang web livestream
        driver.get(f'https://www.tiktok.com/@phuoc19903/live')

        # Chờ tối đa 100 giây để XPATCH được chỉ định xuất hiện, để đảm bảo rằng phiên live đã tải hoàn tất lần 1
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div[1]/a')))

        bot_reply(user_id, "Truy cập phiên live thành công, khi nào phiên live diễn ra tôi sẽ thông báo cho bạn")
        log_success("Truy cập phiên live thành công => TIẾN HÀNH KIỂM TRA THỜI ĐIỂM PHIÊN LIVE ĐƯỢC MỞ")

        # Vòng lặp whilte lặp lại việc kiểm tra số lượng người xem của phiên live cho đến khi nào phiên live được diễn ra thì mới kết thúc vòng lặp lần 1
        while True:
            now = datetime.datetime.now() # Biến lấy ngày giờ hiện tại của hệ thống
            try:
                # Đợi tối đa 10 giây để XPATCH chứa dữ liệu là số lượng người xem của phiên live xuất hiện rồi mới kiểm tra
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[4]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div')))
                
                bot_reply(user_id, f"Check live hoàn tất, phiên live đã được mở vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")
                log_info(f"Phiên live đã được diễn ra vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")

                log_info("Đóng trình duyệt chrome")
                driver.quit()

                log_info("Kết thúc tiến trình")
                return
            except TimeoutException:
                log_error("Phiên live chưa được diễn ra")
                log_info("Làm mới lại phiên live")

                # Làm mới lại phiên live
                driver.refresh()

                # Kiểm tra xem có làm mới lại phiên live thành công hay không
                try:
                    # Chờ tối đa 100 giây để XPATCH được chỉ định xuất hiện, để đảm bảo rằng phiên live đã tải hoàn tất
                    WebDriverWait(driver, 100).until(
                        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[3]/div/div[1]/a"))
                    )
                except TimeoutException:
                    bot_reply(user_id, "Kiểm tra phiên live thất bại, không thể tải phiên live trong thời gian chờ quy định")
                    log_error("Kiểm tra phiên live thất bại, không thể tải phiên live trong thời gian chờ quy định")

                    log_info("Đóng trình duyệt chrome")
                    driver.quit()

                    log_info("Kết thúc tiến trình")
                    return
    except TimeoutError:
        bot_reply(user_id, "Không thể truy cập phiên live, xảy ra sự cố kết nối internet")
        log_info("Không thể truy cập phiên live do kết nối internet")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return    